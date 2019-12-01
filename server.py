
import socket
import time
import threading
from mysqlDataBase import RegisterToDataBase
import os
from datetime import date, datetime


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

                if message[0] == "upload":
                    
                    print("UPLOAD: ", message)
                    self.csocket.send('ok'.encode())
                    destino = "filesUser/"+message[2]+"/"+message[4]+"/"+message[1]

                    f = open(destino,'wb')
                                                            
                    while True:
                        l = self.csocket.recv(1024)
                        
                        while (l):
                            if "done" in str(l):
                                print("Upload Finalizado")
                                self.MYSQL.save_file(message[1],message[4],message[5],message[3])
                                break
                            l = self.csocket.recv(1024)
                            f.write(l)
                        f.close()
                        break
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
                    # Email message[0] Senha message[1]
                    status,user = self.MYSQL.isRegistred(message[1],message[2])
                    
                    if status:
                        response = list()
                        response.append(user[0][0])
                        response.append(user[0][1])
                        response.append(user[0][2])
                        response.append(user[0][3])

                        self.csocket.send(str(response).encode())
                    else:
                        self.csocket.send('error'.encode())

                if message[0] == "get_files":

                    print(message)
                    
                    files = self.MYSQL.get_files(message[1],message[2])
                    
                    a = []
                   
                    for file in files:

                        a.append(";")
                        a.append(file[0])
                        a.append(file[1])
                        a.append(file[2])
                        a.append(file[3])
                        a.append(file[4].strftime('%d/%m/%Y'))
                        a.append(file[5])

                    self.csocket.send(str(a).encode())

            except:
                pass    

if __name__ == '__main__':
    HOST = ''
    PORT = 8000
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