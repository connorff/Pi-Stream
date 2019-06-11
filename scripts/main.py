from flask import Flask, render_template, request, session, redirect, url_for, Response
from flask_session import Session
from db import db_connect
from users_class import User
from camera_class import Camera

app = Flask(__name__, template_folder="../tpl", static_folder="../static")
conn = db_connect()
user = User(conn)

#session stuff
SESSION_TYPE = 'redis'
app.config.from_object(__name__)
Session(app)

def genFunction():
	#forever: uses camera class to get a camera frame and yields it
	while True:
		frame = Camera().get_frame()
		yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/", methods=["POST", "GET"])
def index():
	#if the user submitted the form
	if request.form.get("submit"):
		username = request.form.get("username")
		password = request.form.get("password")
		
		#if the credentials match a user
		if user.login(username, password):
			session["username"] = username
			return redirect(url_for('watch'))
		
	return render_template("index.html")	

#route for a specific user page
@app.route("/user/<username>")
def specUser(username):
	return username

#route that gives a list of all users
@app.route("/user")
def listUsers():
	#array of tuples of users (username, user_level)
	userList = user.listUsers()
	
	return "hi"

#route for the watch page	
@app.route("/watch")
def watch():
	#if the user is not signed in
	if not session.get("username"):
		return redirect(url_for("index"))
	return render_template("watch.html")

#route for just the video (used to display the video to the /watch page)
@app.route("/video_only")
def watch_video_only():
	#if the user is not signed in
	if not session.get("username"):
		return redirect(url_for("index"))
	
	return Response(genFunction(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
	app.run("0.0.0.0", port=8080)
