Last login: Wed Feb 13 02:08:14 on ttys000
swetalis-macbook-air:bookReco_epita thechidiya$ flask run
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
Usage: flask run [OPTIONS]

Error: Could not locate a Flask application. You did not provide the "FLASK_APP" environment variable, and a "wsgi.py" or "app.py" module was not found in the current directory.
swetalis-macbook-air:bookReco_epita thechidiya$ pwd
/Users/thechidiya/Python/bookReco_epita
swetalis-macbook-air:bookReco_epita thechidiya$ vi application.py 
swetalis-macbook-air:bookReco_epita thechidiya$ vi export.txt 
swetalis-macbook-air:bookReco_epita thechidiya$ vi application.py 
swetalis-macbook-air:bookReco_epita thechidiya$ vi templates/index.html 
swetalis-macbook-air:bookReco_epita thechidiya$ vi application.py 
swetalis-macbook-air:bookReco_epita thechidiya$ vi templates/index.html 
swetalis-macbook-air:bookReco_epita thechidiya$ vi application.py 
swetalis-macbook-air:bookReco_epita thechidiya$ vi templates/index.html 
swetalis-macbook-air:bookReco_epita thechidiya$ touch templates/dashboard.html
swetalis-macbook-air:bookReco_epita thechidiya$ vi application.py 
swetalis-macbook-air:bookReco_epita thechidiya$ vi application.py 
















import os
import requests

from flask import Flask, render_template, flash, request, url_for, redirect, Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from wtforms import Form, BooleanField, TextField, PasswordField, validators

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

#set up registeration form
class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice (updated Jan 22, 2015)', [validators.Required()])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard",methods=["POST"] )
def login():
  username = request.form.get("username")
  password = request.form.get("passwd");
  isExist = db.execute("SELECT username FROM users WHERE (username=username) AND (password=password)")
  if int(isExist) > 0:
    return render_template("dashboard.html")
  else:
    return render_template("register.html")

@app.route("/register",methods=["GET", "POST"] )
def register_page():
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            username  = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            c, conn = connection()

            x = c.execute("SELECT * FROM users WHERE username = (%s)",
                          (thwart(username)))




