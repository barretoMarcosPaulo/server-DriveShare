import socket
import time
import threading
from mysqlDataBase import RegisterToDataBase
import os
class ServerSide():
	def __init__(self):
		self.host = ""
		self.port = 3000
		self.address = (self.host,self.port)
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.connection = ""
		self.clients = set()
		self.MYSQL = RegisterToDataBase()
		self.defaultPath = "filesUser/"
	def run_server(self):
		
		print("Server Started")
		
		self.server_socket.bind(self.address)
		self.server_socket.listen(10)
		self.receive_connections()

	def receive_connections(self):

		print("Await Connection...")
		while True:
			self.connection,c = self.server_socket.accept()	
			# self.connection.send('WELCOME'.encode())	
			self.clients.add(self.connection)
			print(self.connection)
			threading.Thread(target=self.receive_datas, args=(self.clients,)).start()


	def receive_datas(self,*args, **kwargs):
		print("Await datas...")
		while True:
			try:
				recebe = self.connection.recv(1024).decode() 
				recebe = recebe.split(',')
				if recebe[0] == "register":
					if self.MYSQL.email_is_regitred(recebe[3]):
						self.connection.send('error'.encode())
					else:
						
						path ="filesUser/"+recebe[3]
						os.mkdir(path)
						os.mkdir(path+"/documentos")
						os.mkdir(path+"/imagens")
						os.mkdir(path+"/musicas")
						os.mkdir(path+"/videos")
						os.mkdir(path+"/outros")
						os.mkdir(path+"/compartilhados")
						print(recebe)
						self.MYSQL.save_datas(recebe[1],recebe[2],recebe[3],recebe[4])
						self.connection.send('ok'.encode())
						

				if recebe[0] == "login":
					print(recebe[1], recebe[2])

					if self.MYSQL.isRegistred(recebe[1],recebe[2]):
						self.connection.send('ok'.encode())
					else:
						self.connection.send('error'.encode())

				# for c in self.clients:
				# 	c.send('Estou no For'.encode())
			except:
				break


	def stop_server(self):
		self.server_socket.close()

Server = ServerSide()
Server.run_server() 



