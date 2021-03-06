import socket 
import time
from datetime import datetime

class ClientSide():
	def __init__(self):
		# self.host = '168.235.110.16'
		self.host = 'localhost'
		self.port = 8000
		self.address=((self.host,self.port))
		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		self.connect()

	def connect(self):
		connected = True
		try:
			self.client_socket.connect(self.address)
		except:
			connected = self.reestablish_connection()
		return connected


	def reestablish_connection(self):
		connection_attempt = 0
		connected = False
		while(connection_attempt<5):
			try:
				print("try connection...")
				time.sleep(2)
				self.client_socket.connect(self.address)
				connected = True
				break
			except:
				connection_attempt+=1
		return connected


	def sendDatas(self,content):
				
		self.client_socket.send(content.encode()) 
		# Return error/success and message
		
		resposta = self.client_socket.recv(1024).decode()
		
		if resposta == "error":
			return False
		if resposta == "ok":
			retur