
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

	def shared_register(self,user_shared , file , user_receive):

		current_date = date.today()

		try:
			print("Conectando")
			cursor = self.connection.cursor()
			query = "INSERT INTO shared( user_shared, file_id, user_receive, date_shared) VALUES(%s,%s,%s,%s)"
			
			print("Salvando")
			cursor.execute(query,(user_shared , file , user_receive , current_date))
			self.connection.commit()
			print("Ok")
			return True

		except:
			print("Connection Error!!!")
			return False

	def get_files_shared(self , email):

		cursor = self.connection.cursor()
		
		querySelect = "SELECT users.primaryName, users.email,files.filename,files.size FROM shared INNER JOIN users ON users.id = shared.user_receive INNER JOIN files ON files.id = shared.file_id"

		cursor.execute(querySelect)
		shareds = cursor.fetchall()
		list_current_user = []

		if len(shareds) > 0:
			print("ACHOU S")
			for s in shareds:
				if s[1]==email:
					list_current_user.append(s)

			return True,list(list_current_user)
		else:
			print("ACHOU N")
			return False,list(list_current_user)

	def my_shared_files(self,user_id):
		
		cursor = self.connection.cursor()
		querySelect = "SELECT * FROM shared WHERE user_receive=%s"
		cursor.execute(querySelect,(user_id))
		files = cursor.fetchall()

		return files


	def user_shared(self, user_id):
		cursor = self.connection.cursor()
		querySelect = "SELECT primaryName,email FROM users WHERE id=%s"
		cursor.execute(querySelect,(user_id))
		user = cursor.fetchall()

		return user

	
	def file_shared(self, file_id):
		cursor = self.connection.cursor()
		querySelect = "SELECT filename,filetype FROM files WHERE id=%s"
		cursor.execute(querySelect,(file_id))
		file = cursor.fetchall()

		return file