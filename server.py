import socket
from mysqlDataBase import RegisterToDataBase

class ServerSide():
	def __init__(self):
		
		self.MYSQL = RegisterToDataBase()

		self.host = ''
		self.port = 7000
		self.addr=(self.host , self.port)
		self.client = ''
		self.connection = ''
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	def startServer(self):
		self.server_socket.bind(self.addr)		
		self.server_socket.listen(10)
		
		while True:
			print('Await Connection...')
			self.connection,self.client = self.server_socket.accept()
			print('Connected , Client = ', self.client)
			self.receiveDatas()
	
	def stopServer(self):
		self.server_socket.close()

	def receiveDatas(self):

		received = self.connection.recv(1024)
		data_received = received.decode() 
		data_received = data_received.split(',') 
	    
		isRegistred = "Ok"

		if data_received[0] == "Register":
			if not self.MYSQL.email_is_regitred(data_received[4]):
				self.MYSQL.save_datas(
					data_received[1], 
					data_received[2], 
					data_received[4], 
					data_received[3], 
				)
				self.connection.send(isRegistred.encode())
			else:
				isRegistred ="Error"
				self.connection.send(isRegistred.encode())
		else:
			print(data_received)

driveShare = ServerSide()
driveShare.startServer()