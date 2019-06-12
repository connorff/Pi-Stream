import mysql.connector
from users_class import User
from comments_class import Comments

def db_connect():
	connection = mysql.connector.connect(
		host = "localhost",
		user = "picamera",
		passwd = "pi",
		db = "picamera"
	)
	
	return connection

#conn = db_connect()	
#conn = db_connect()	
#user = User(conn)
#comments = Comments(conn, user)
