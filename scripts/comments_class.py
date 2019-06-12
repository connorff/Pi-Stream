import time

class Comments:
	def __init__(self, conn, user):
		self.conn = conn
		self.db = self.conn.cursor()
		self.user = user
		
	def post(self, user_id, content):
		if not self.user.checkIfIdExists(user_id):
			return False
			
		sql = "INSERT into comments (user_id, content, time) VALUES (%s, %s, %s);"
		
		self.db.execute(sql, (user_id, content, time.time(),))
		self.conn.commit()
		
	def getAll(self, limit = False):
		if limit != False:
			sql = "SELECT * FROM comments LIMIT %s;"
		else:
			sql = "SELECT * FROM comments;"
		
		self.db.execute(sql)
		arr = []
		for post in self.db.fetchall():
			arr.append([post[0], self.user.getUsernameById(post[1])[0], self.getTime(post[2]), post[3], post[1]])
		return arr
		
	def getByUserId(self, user_id):
		sql = "SELECT * FROM comments WHERE user_id = %s;"
		
		self.db.execute(sql, (user_id,))
		return self.db.fetchall()
		
	def getAfterId(self, comment_id):
		sql = "SELECT * FROM comments WHERE comment_id > %s;"
		
		self.db.execute(sql, (comment_id,))
		
		arr = []
		for post in self.db.fetchall():
			arr.append([post[0], self.user.getUsernameById(post[1])[0], self.getTime(post[2]), post[3], post[1]])
		return arr
		
		return arr
	
	def getTime(self, timestamp):
		currtime = int(time.time())
		
		diff = currtime - timestamp
		
		if diff < 60:
			return "Less than a minute ago"
		elif diff < 3600:
			return "About %s minutes ago" % (int(diff / 60))
		elif diff < 86400:
			return "About %s hours ago" % (int(diff / 3600))
		elif diff < 31536000:
			print "About %s days ago" & (int(diff / 86400))
		else:
			print "More than a year ago"
