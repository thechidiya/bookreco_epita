import os
import requests

from flask import Flask, render_template, flash, request, url_for, redirect, session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from wtforms import Form, BooleanField, TextField, PasswordField, validators

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# set up API KEY from goodreads.com
api_key = os.getenv("API_KEY_GOODREADS")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config["SESSION_TYPE"] = "filesystem"

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods=["GET", "POST"] )
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("passwd")
        x = db.execute("SELECT username FROM users WHERE (username=username) AND (password=password)")
        counter = 0
        for row in x:
            counter = counter + 1
        if int(counter) > 0:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template("login.html")
    else:
        return render_template("login.html")

@app.route("/logout", methods = ['POST', 'GET'])
def logout():
    #Log user out
    # Forget any user_id
    session.clear()
    # Redirect user to default
    return redirect("/login")

@app.route("/register",methods=["GET", "POST"] )
def register():
    return render_template("register.html")

@app.route("/register_user",methods=["POST"] )
def register_user():
    #register user
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        x = db.execute("SELECT * FROM users WHERE (username = " + username + ")")
        counter = 0
        for row in x:
            counter = counter + 1
        if int(counter) > 0:
            flash("Username is taken, please select another")
            return render_template("register.html")
        elif password1 != password2:
            flash("Passwords do not match, try again")
            return render_template("register.html")
        elif not email:
            flash("Please enter email")
            return render_template("register.html")
        else:
            db.execute("INSERT INTO users (username, password, email) VALUES ('"+username+"', '"+password1+"', '"+email+"')")
            db.commit()
            flash("Thanks for registering!")
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))

@app.route("/dashboard",methods=["GET", "POST"] )
def dashboard():
    try:
        data = db.execute("SELECT * from books")        
        return render_template("dashboard.html", data=data)
        
    except Exception as e:
        return (str(e))

@app.route("/search",methods=["GET", "POST"] )
def search():
    if request.method == "POST":
        isbn = request.form.get("isbn")
        title = request.form.get("title")
        author = request.form.get("author")
        year = request.form.get("year")
        str_sql = "SELECT * FROM books WHERE 1=1"
        if isbn:
            str_sql += " AND (isbn='"+isbn+"')"
        if title:
            str_sql += " AND (title='"+title+"')"
        if author:
            str_sql += " AND (author='"+author+"')"
        if year:
            str_sql += " AND (year='"+year+"')"
        data = db.execute(str_sql)
        print(str_sql)
        return render_template("dashboard.html", data=data)


