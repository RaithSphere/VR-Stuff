using Ninja.WebSockets;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Net.WebSockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace HeartRate
{
    class WebSocketComponent
    {
        private static List<WebSocket> clients = new List<WebSocket>();
        private static WebSocketServerFactory factory = new WebSocketServerFactory();

        private static async Task AcceptClient(TcpClient tcpClient)
        {
            using (tcpClient)
            {
                var stream = tcpClient.GetStream();
                try
                {
                    var context = await factory.ReadHttpHeaderFromStreamAsync(stream);
                    if (context.IsWebSocketRequest)
                    {

                        var buffer = new ArraySegment<byte>(new byte[1024]);
                        var client = await factory.AcceptWebSocketAsync(context);

                        try
                        {
                            var source = (tcpClient.Client.RemoteEndPoint as IPEndPoint)?.Address.ToString();
                            Console.WriteLine($"Connection from {source ?? "unknown"}");
                            lock (clients)
                            {
                                clients.Add(client);
                            }
                            ClientChange?.Invoke(typeof(WebSocketComponent), EventArgs.Empty);
                            Connected?.Invoke(typeof(WebSocketComponent), new ConnectedEventArgs(client));
                            while (client.State == WebSocketState.Open)
                            {
                                var message = await client.ReceiveAsync(buffer, CancellationToken.None);
                                switch (message.MessageType)
                                {
                                    case WebSocketMessageType.Close:
                                        await client.CloseAsync(WebSocketCloseStatus.NormalClosure, null, CancellationToken.None);
                                        break;
                                }
                            }
                        }
                        finally
                        {
                            bool change;
                            lock (clients)
                            {
                                change = clients.Remove(client);
                            }
                            if (change)
                            {
                                ClientChange?.Invoke(typeof(WebSocketComponent), EventArgs.Empty);
                            }
                        }
                    }
                }
                finally
                {
                    stream.Close();
                    tcpClient.Close();
                }
            }
        }

        public static event EventHandler? ClientChange;

        public class ConnectedEventArgs : EventArgs
        {
            public ConnectedEventArgs(WebSocket client)
            {
                Client = client;
            }

            public WebSocket Client { get; set; }
        }

        public static event EventHandler<ConnectedEventArgs>? Connected;

        private static bool running = true;
        private static TcpListener? tcpListener1;

        public static bool Running => running;

        public static int ClientsCount
        {
            get
            {
                lock (clients)
                {
                    return clients.Count;
                }
            }
        }

        private static Encoding utf8 = new UTF8Encoding(false);

        public static Task SendMessage(WebSocket client, string message)
        {
            var bytes = new ArraySegment<byte>(utf8.GetBytes(message));

            return client.SendAsync(bytes, WebSocketMessageType.Text, true, CancellationToken.None);
        }

        public static Task SendMessage(string message)
        {
            return SendMessage(new ArraySegment<byte>(utf8.GetBytes(message)));
        }

        public static async Task SendMessage(ArraySegment<byte> message)
        {
            var remove = new List<int>();
            var sends = new List<Task>();
            bool clientsChange;
            lock (clients)
            {
                for (int i = 0; i < clients.Count; ++i)
                {
                    var client = clients[i];
                    if (client.State == WebSocketState.Open)
                    {
                        try
                        {
                            sends.Add(client.SendAsync(message, WebSocketMessageType.Text, true, CancellationToken.None));
                        }
                        catch (Exception ex)
                        {
                            Trace.WriteLine($"{ex} in sending");
                        }
                    }
                    else
                    {
                        remove.Add(i);
                    }
                }
                clientsChange = remove.Count > 0;
                if (clientsChange)
                {
                    remove.Sort();
                    remove.Reverse();
                    foreach (var i in remove)
                    {
                        clients.RemoveAt(i);
                    }
                }
            }
            if (clientsChange)
            {
                ClientChange?.Invoke(typeof(WebSocketComponent), EventArgs.Empty);
            }
            try
            {
                await Task.WhenAll(sends);
            }
            catch (Exception ex)
            {
                Trace.WriteLine($"{ex} while waiting");
            }
        }

        public static async Task Start(int port)
        {
            DebugLog.WriteLog("Starting Websocket Client");

            if (tcpListener1 != null)
            {
                throw new InvalidOperationException("WebSocketComponent already started");
            }
            tcpListener1 = new TcpListener(System.Net.IPAddress.Loopback, port);
            tcpListener1.Start();
            while (running)
            {
                var tcpClient = await tcpListener1.AcceptTcpClientAsync();
                _ = Task.Run(() => AcceptClient(tcpClient));
            }
        }

        public static Task Stop()
        {
            return Stop(CancellationToken.None);
        }

        public static Task Stop(CancellationToken cancellationToken)
        {
            tcpListener1?.Stop();
            tcpListener1 = null;

            WebSocket[] oldClients;
            lock (clients)
            {
                oldClients = new WebSocket[clients.Count];
                clients.CopyTo(oldClients);
                clients.Clear();
            }

            return Task.WhenAll(oldClients.Where(c => c.State == WebSocketState.Open).Select(c => c.CloseAsync(WebSocketCloseStatus.NormalClosure, "Stopped", cancellationToken)))
                .ContinueWith(task => {
                    foreach (var client in oldClients.Where(c => c.State != WebSocketState.Closed && c.State != WebSocketState.Aborted && c.State != WebSocketState.None))
                    {
                        client.Abort();
                    }
                }, CancellationToken.None);
        }
    }
}
