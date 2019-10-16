# import socket
# import time
# import threading
# from mysqlDataBase import RegisterToDataBase
# import os
# class ServerSide():
#   def __init__(self):
#       self.host = ""
#       self.port = 3000
#       self.address = (self.host,self.port)
#       self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#       self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#       self.csocket = ""
#       self.clients = set()
#       self.MYSQL = RegisterToDataBase()
#       self.defaultPath = "filesUser/"
#   def run_server(self):
        
#       print("Server Started")
        
#       self.server_socket.bind(self.address)
#       self.server_socket.listen(10)
#       self.receive_csockets()

#   def receive_csockets(self):

#       print("Await Connection...")
#       while True:
#           self.csocket,c = self.server_socket.accept() 
#           # self.csocket.send('WELCOME'.encode())  
#           self.clients.add(self.csocket)
#           print(self.csocket)
#           threading.Thread(target=self.receive_datas, args=(self.clients,)).start()


#   def receive_datas(self,*args, **kwargs):
#       print("Await datas...")
#       while True:
#           try:
#               message = self.csocket.recv(1024).decode() 
#               message = message.split(',')
#               if message[0] == "register":
#                   print(message)
#                   # if self.MYSQL.email_is_regitred(message[3]):
#                   #   self.csocket.send('error'.encode())
#                   # else:
                        
#                   #   path ="filesUser/"+message[3]
#                   #   os.mkdir(path)
#                   #   os.mkdir(path+"/documentos")
#                   #   os.mkdir(path+"/imagens")
#                   #   os.mkdir(path+"/musicas")
#                   #   os.mkdir(path+"/videos")
#                   #   os.mkdir(path+"/outros")
#                   #   os.mkdir(path+"/compartilhados")
#                   #   print(message)
#                   #   self.MYSQL.save_datas(message[1],message[2],message[3],message[4])
#                   self.csocket.send('ok'.encode())
                        

#               if message[0] == "login":
#                   print(message[1], message[2])
#                   self.csocket.send('ok'.encode())
#                   # if self.MYSQL.isRegistred(message[1],message[2]):
#                   #   self.csocket.send('ok'.encode())
#                   # else:
#                   #   self.csocket.send('error'.encode())

#               # for c in self.clients:
#               #   c.send('Estou no For'.encode())
#           else:
#               print(message)
#           except:
#               break


#   def stop_server(self):
#       self.server_socket.close()

# Server = ServerSide()
# Server.run_server() 



import socket
import time
import threading
from mysqlDataBase import RegisterToDataBase
import os

class ServerSide(threading.Thread):
    def __init__(self,clientAddress,clientsocket):

        threading.Thread.__init__(self)
        self.csocket = clientsocket



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
                    print ("Recebido", message)
                    # if self.MYSQL.email_is_regitred(message[3]):
                    #     self.csocket.send('error'.encode())
                    # else:
                    print("OKKKK")
                    path ="filesUser/"+message[3]
                    os.mkdir(path)
                    os.mkdir(path+"/documentos")
                    os.mkdir(path+"/imagens")
                    os.mkdir(path+"/musicas")
                    os.mkdir(path+"/videos")
                    os.mkdir(path+"/outros")
                    os.mkdir(path+"/compartilhados")
                    print(message)
                    # self.MYSQL.save_datas(message[1],message[2],message[3],message[4])
                    self.csocket.send('ok'.encode())
                
                if message[0] == 'login':
                    print(message)
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

    while True:
        server.listen(1)
        clientsock, clientAddress = server.accept()
        newthread = ServerSide(clientAddress, clientsock)
        newthread.start()