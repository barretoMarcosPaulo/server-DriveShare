import socket
import time
import threading
from mysqlDataBase import RegisterToDataBase

class ServerSide():
	def __init__(self):
		self.host = ""
		self.port = 3000
		self.address = (self.host,self.port)
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.connection = ""
		self.clients = set()

	def run_server(self):
		
		print("Server Started")
		
		self.server_socket.bind(self.address)
		self.server_socket.listen(10)
		self.receive_connections()

	def receive_datas(self,*args, **kwargs):
		print("Await datas...")
		while True:
			try:
				recebe = self.connection.recv(1024) 
				print(recebe.decode())
				for c in self.clients:
					c.send('HELLO'.encode())
			except:
				break

		
	def receive_connections(self):

		print("Await Connection...")
		while True:
			self.connection,c = self.server_socket.accept()	
			self.connection.send('WELCOME'.encode())		
			self.clients.add(self.connection)
			threading.Thread(target=self.receive_datas, args=(self.clients,)).start()

	def stop_server(self):
		self.server_socket.close()

Server = ServerSide()
Server.run_server() 



