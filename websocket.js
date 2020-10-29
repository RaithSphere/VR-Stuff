print("--Starting NeosHeart Websocket Server Process--")

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

class SimpleEcho(WebSocket):

    def handleMessage(self):
        hrbt = open("hrbt.txt","r")
        data = hrbt.read()
        self.sendMessage(data)
        hrbt.close()

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')

server = SimpleWebSocketServer('', 8123, SimpleEcho)
server.serveforever()
