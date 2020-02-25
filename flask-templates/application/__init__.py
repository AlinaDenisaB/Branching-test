 # import Flask class from the flask module
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from os import getenv
from flask_bcrypt import Bcrypt

 # create a new instance of Flask and store it in app 
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://alina:password@127.0.0.1/db"
app.config['SECRET_KEY'] = str(os.getenv('MY_SECRET_KEY'))
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

 # import the ./application/routes.py file
from application import routes

