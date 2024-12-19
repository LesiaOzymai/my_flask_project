#models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Accounts(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False, unique=True)
    balance = db.Column(db.Float, default=0.0, nullable=False)