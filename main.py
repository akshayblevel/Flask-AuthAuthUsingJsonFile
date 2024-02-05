from flask import Flask, session, request, redirect, url_for, render_template
import json

users_path = "./users.json"
marks_path = "./marks.json"

users = json.load(open(users_path,mode='r'))
marks = json.load(open(marks_path,mode='r'))


app = Flask(__name__)


app.secret_key = "###secretkey###"

 
@app.route('/', methods=["GET"])
def login():
   if "username" in session:
       return redirect(url_for("user",name=session["username"]))

   if not("try" in session): session["try"] = 0

   if session["try"] < 3:
       error = False
       if session["try"] > 0:
           error = True

       return render_template("login.html",error=error)
   return redirect(url_for("failure"))

 
@app.route('/authenticator', methods=['POST'])
def authenticator():
   if "username" in session:
       return redirect(url_for("user",name=session["username"]))

   if "try" in session and session["try"] < 3:
       username = request.form.get('name')
       password = request.form.get('pass')

       if username in users and password == users[username]:
           session["username"] = username
           return redirect(url_for("user",name=username))

       session["try"] += 1

       return redirect(url_for("login", username=username))
   return redirect(url_for("login"))

 
@app.route('/user/<name>')
def user(name):
   if "username" in session:
       user_mark = marks.get(name)
       return render_template("success.html", name=name, marks = user_mark)
   return redirect(url_for("login"))

 
@app.route('/failure')
def failure():
   if "username" in session:
       return redirect(url_for("user",name=session["username"]))

   if "try" in session and session["try"] < 3:
       return redirect(url_for("login"))

   return render_template("failure.html")

 

@app.route('/logout')
def logout():
   session.pop("try")

   if "username" in session:
       session.pop("username")

   return redirect(url_for("login"))


app.run(debug=True)