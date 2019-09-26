
import pymysql


class RegisterToDataBase():
	def __init__(self):
		self.host = 'localhost'
		self.database = 'drive'
		self.user = 'driveshare'
		self.passwd = 'drive@123'
		self.connection = pymysql.connect(host=self.host,db=self.database, user=self.user, passwd=self.passwd)


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
			res = True
		else:
			res = False
		return res	
