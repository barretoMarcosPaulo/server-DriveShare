
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

                if message[0] == "upload":

                    print("Upload",message[1])
                    print("Pasta de upload ",message[2])
                    
                    self.csocket.send('ok'.encode())
                    path = "filesUser/"+message[2]+"/"+message[1]
                    print(path)
                    f = open(path,'wb')
                    
                                        
                    while True:
                        l = self.csocket.recv(1024)
                        
                        while (l):
                            print("Receiving... ")
                            
                            if "done" in str(l):
                                print("Upload Finalizado")
                                break
                            l = self.csocket.recv(1024)
                            f.write(l)
                        f.close()

                        print("FORA")
                        
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