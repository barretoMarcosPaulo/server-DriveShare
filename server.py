
import socket
import time
import threading
from mysqlDataBase import RegisterToDataBase
import os

class ServerSide(threading.Thread):
    def __init__(self,clientAddress,clientsocket,database):

        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.MYSQL = database


        print ("Cliente Conectado: ", clientAddress)
    
    def run(self):
        print ("Aguardando dados de: ", clientAddress)
        
        message = ''
        
        while True:
            try:
                data = self.csocket.recv(1024)
                message = data.decode()
                message = message.split(',')

                if message[0] == "register":

                    # if self.MYSQL.email_is_regitred(message[3]):
                    #     self.csocket.send('error'.encode())
                    # else:
    
                    path ="filesUser/"+message[3]
                    os.mkdir(path)
                    os.mkdir(path+"/documentos")
                    os.mkdir(path+"/imagens")
                    os.mkdir(path+"/musicas")
                    os.mkdir(path+"/videos")
                    os.mkdir(path+"/outros")
                    os.mkdir(path+"/compartilhados")
                    print(message)
                    self.MYSQL.save_datas(message[1],message[2],message[3],message[4])
                    self.csocket.send('ok'.encode())
                
                if message[0] == 'login':

                    self.csocket.send('ok'.encode())
            except:
                pass    

if __name__ == '__main__':
    HOST = ''
    PORT = 3000
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    print("Servidor iniciado!")
    print("Aguardando nova conexao..")
    
    database = RegisterToDataBase()
    database.connect()

    while True:
        server.listen(1)
        clientsock, clientAddress = server.accept()
        newthread = ServerSide(clientAddress, clientsock , database)
        newthread.start()