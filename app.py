# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from src.config import APP_CONFIG

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://buildcraftuser:buildcraftpassword@localhost/buildcraftdb"
# Replace 'username', 'password', 'localhost', and 'db_name' with your PostgreSQL credentials
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
