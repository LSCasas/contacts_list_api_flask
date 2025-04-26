from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import mapped_column
from contacts_list.db import db


class User(db.Model):
    """User Object  """
    __tablename__ = 'users'
    id_user = mapped_column(Integer, primary_key=True)
    username = db.Column(String(length=50), unique=True, nullable=False)
    email = db.Column(String, unique=True, nullable=False)
    password = db.Column(String, nullable=False)
    phone = db.Column(String(length=50))
    address = db.Column(String)


class Contact(db.Model):
    """Contact model related to a user"""
    __tablename__ = 'contacts'
    id_contact = mapped_column(Integer, primary_key=True)
    name = db.Column(String(50), nullable=False)
    email = db.Column(String(50), nullable=False)
    phone = db.Column(String(length=50), nullable=False)
    address = db.Column(String)
