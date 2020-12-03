from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket


class SimpleEcho(WebSocket):

    def handleMessage(self):
        print(self.data)
        file = self.data
        textfile = open("%s" % file)
        data = textfile.read()
        self.sendMessage(data)
        textfile.close()


    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')


server = SimpleWebSocketServer('', 8123, SimpleEcho)
server.serveforever()
