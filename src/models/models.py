# models.py
from app import db

class Building(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    coordinates = db.Column(db.String(50))
