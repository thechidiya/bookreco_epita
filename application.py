import os
import requests

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

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


