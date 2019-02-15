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
        isExist = db.execute("SELECT username FROM users WHERE (username=username) AND (password=password)")
        if int(isExist) > 0:
            return render_template("dashboard.html")
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
    return redirect("/")

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
        x = db.execute("SELECT * FROM users WHERE (username = username)")
        if int(x) > 0 or password1 != password2:
            flash("Username is taken, please select another or password doesn't match")
            return render_template("register.html")
    else:
        db.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)")
        db.commit()
        flash("Thanks for registering!")
        session['logged_in'] = True
        session['username'] = username
        return redirect(url_for('dashboard'))

@app.route("/dashboard",methods=["GET", "POST"] )
def dashboard():
    try:
        db.execute("SELECT * from books")
        data = db.fetchall()
        return data
        
        return render_template("dashboard.html", data=data)
        
    except Exception as e:
        return (str(e))


