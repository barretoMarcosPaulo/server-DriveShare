
import pymysql
from datetime import date

class RegisterToDataBase():
	def __init__(self):
		self.host = 'localhost'
		self.database = 'drive'
		self.user = 'drive'
		self.passwd = 'drive@123'
		self.connection = " "

	def connect(self):
		print("Conectado ao Banco de Dados")
		self.connection = pymysql.connect(host=self.host,db=self.database, user=self.user, passwd=self.passwd)
	
	def disconnect(self):
		self.connection.close()

	def save_datas(self , name , lastname , email , password):
		
		name = name
		lastname = lastname
		email = email
		password = password

		try:
			cursor = self.connection.cursor()
			querySaveUser = "INSERT INTO users(primaryName,lastName,email,passwd) VALUES(%s,%s,%s,%s)"
			
			try:
				cursor.execute(querySaveUser,(name,lastname,email,password))
				self.connection.commit()
				
			except:
				print("Error!!!")
		except:
			print("Connection Error!!!")

	def save_file(self,filename,filetype,size,user_id):

		current_date = date.today()

		try:
			print("Conectando")
			cursor = self.connection.cursor()
			query = "INSERT INTO files(filename,filetype,size,date_upload,user_id) VALUES(%s,%s,%s,%s,%s)"
			
			print("Salvando")
			cursor.execute(query,(filename,filetype,size,current_date,user_id))
			self.connection.commit()
			print("Ok")

		except:
			print("Connection Error!!!")


	def email_is_regitred(self,email):
		cursor = self.connection.cursor()
		cursor.execute("SELECT * FROM users WHERE email=%s",email)
		users = cursor.fetchall()
		if len(users) > 0:
			res = True
		else:
			res = False
		return res

	def isRegistred(self,email,passwds):
		cursor = self.connection.cursor()
		querySelect = "SELECT * FROM users WHERE email=%s AND passwd=%s"
		cursor.execute(querySelect,(email,passwds))
		users = cursor.fetchall()
		

		if len(users) > 0:
			print("ACHOU S")
			return True,list(users)
		else:
			print("ACHOU N")
			return False,list(users)
	
	def get_files(self, type_file, user_id):

		files = []

		if type_file == "recentes":

			cursor = self.connection.cursor()
			querySelect = "SELECT * FROM files WHERE user_id=%s order by id desc LIMIT 15"
			cursor.execute(querySelect,(user_id))
			files = cursor.fetchall()

		else:

			cursor = self.connection.cursor()
			querySelect = "SELECT * FROM files WHERE filetype=%s AND user_id=%s"
			cursor.execute(querySelect,(type_file,user_id))
			files = cursor.fetchall()

		return files

	def user_exists(self,email):

		cursor = self.connection.cursor()
		querySelect = "SELECT * FROM users WHERE email=%s"
		cursor.execute(querySelect,(email))
		users = cursor.fetchall()
		
		if len(users) > 0:
			print("ACHOU S")
			return True,list(users)
		else:
			print("ACHOU N")
			return False,list(users)
