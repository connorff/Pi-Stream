import mysql.connector
from users_class import User

def db_connect():
	connection = mysql.connector.connect(
		host = "localhost",
		user = "picamera",
		passwd = "pi",
		db = "picamera"
	)
	
	return connection
