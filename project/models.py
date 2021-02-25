# models.py

from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100))
    firstname = db.Column(db.String(100), nullable=False, server_default='')
    lastname = db.Column(db.String(100), nullable=False, server_default='')
    phonenumber = db.Column(db.String(20), nullable=False, server_default='')
    address = db.Clomn(db.String(20), nullable=False, server_default='')

# Define the Role data model
class Admin(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

class Staff(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

class Order(db.Model):
    orderId = db.Column(db.Integer(), primary_key=True)
    userId = db.Column(db.Integer(), ForeignKey('user.id'))
    checkoutTime = db.Column(db.DateTime, nullable=False, server_default=datetime.utcnow)
    pickup = db.Column(db.Boolean, nullable=False, server_default=False)
    pickupTime = db.Column(db.DateTime, nullable=True, server_default=datetime.utcnow)
    orderStatus = db.Column(db.String(30), nullable=False, server_default='Preparing')
    bill_amount = db.Column(db.Numeric(8,2), nullable=False, server_default=0.00)
    
    def __init__(self, userId):
        self.userId = userId