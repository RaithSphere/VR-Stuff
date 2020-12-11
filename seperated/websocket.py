import json
import os

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

data = "";


def loadwhitelist():
    global data
    confpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "whitelist.json")
    if os.path.exists(confpath):
        with open("whitelist.json") as json_data_file:
            data = json.load(json_data_file)
    else:
        print("No Config file found")
        exit(0)


class SimpleEcho(WebSocket):

    def handleMessage(self):
        global data
        loadwhitelist()

        filename = self.data.rsplit('\\', 1)[-1]

        if filename in data['whitelist']:
            print(self.data)
            file = self.data
            textfile = open("%s" % file)
            data = textfile.read()
            self.sendMessage(data)
            textfile.close()
        else:
            self.sendMessage("Access to this file is not allowed under whitelist policy")
            print("Not found on whitelist %s" % self.data)

    def handleConnected(self):
        print(self.address, "connected")

    def handleClose(self):
        print(self.address, "closed")


print("Starting Simple Websocket")
server = SimpleWebSocketServer("", 8123, SimpleEcho)
server.serveforever()
