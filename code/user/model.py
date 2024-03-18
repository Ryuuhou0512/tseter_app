from db import db
from app import app
from flask_login import login_user, UserMixin


class user(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    serial_number = db.Column(db.Integer, nullable=False)
    is_deleted = db.Column(db.Integer, default=1)


