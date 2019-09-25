import socket

class ServerSide():
	def __init__(self):
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
		print('Await Connection...')
		self.connection,self.client = self.server_socket.accept()
		print('Connected , Client = ', self.client)
		self.receiveDatas()
	
	def stopServer(self):
		self.server_socket.close()

	def receiveDatas(self):
	    received = self.connection.recv(1024)
	    print(received.decode())

driveShare = ServerSide()
driveShare.startServer()