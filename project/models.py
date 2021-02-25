# models.py

from flask_login import UserMixin
from . import db
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(255, collation='NOCASE'), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100))
    firstname = db.Column(db.String(100), nullable=False, server_default='')
    lastname = db.Column(db.String(100), nullable=False, server_default='')
    phonenumber = db.Column(db.String(20), nullable=False, server_default='')
    address = db.Clomn(db.String(20), nullable=False, server_default='')
    payment = db.Clomn(db.String(20), nullable=False, server_default='')
    plateNum = db.Column(db.String(10), nullable=True, server_default='')
    carDescription = db.Column(db.String(100), nullable=True, server_default='color and band')
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    def __init__(self,email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    

# Define the Role data model
class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    # Relationships
    users = db.relationship('User', backref='role')

class MenuItem(db.Model):
    __tablename__ = 'menu_item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    price = db.Column(db.Numeric(5,2), nullable=False, server_default=0.00)
    stock = db.Column(db.Integer, nullable=False, server_default=10)
    category = db.Column(db.String(20), nullable=False, server_default='')
    picture = db.Clomn(db.String(60), nullable=False, server_default='default.jpg')

    def __init__(self,name,price, availability, picture):
        self.name = name
        self.price = price
        self.stock = stock
        
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
    
    
class OrderItem(db.Model):       
    __tablename__ = 'order_items'
    id = db.Column(db.Integer(), primary_key=True)
    order_id = db.Column(db.Integer(), ForeignKey('order.id', ondelete='CASCADE'))
    food_id = db.Column(db.Integer(), ForeignKey('menu_item.id', ondelete='CASCADE'))  
    food_qty = db.Column(db.Integer(), nullable=False, server_default=0)
    
    items = db.relationship('MenuItem', backref='menu_item')

    def __init__(self, order_id, food_id, food_qty):
        self.order_id = order_id
        self.food_id = food_id
        self.food_qty = food_qty

   