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
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    def __init__(self,email,password):
        self.email = email
        self.password_hash = generate_password_hash(password)

    

# Define the Role data model
class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    # Relationships
    users = db.relationship('User', backref='role')

class Menu(db.Model):
    name = db.Column(db.String(50), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False, server_default=0)
    availability = db.Column(db.Boolean, nullable=False, server_default=True)
    picture = db.Clomn(db.String(60), nullable=False, server_default='default.jpg')

    def __init__(self,name,price, availability, picture):
        self.name = name
        self.price = price
        self.availability = availability
        self.picture = picture
    

# The Admin page requires an 'Admin' role.
    @app.route('/admin/modifyMenu')
    @roles_required('Admin')    # Use of @roles_required decorator
    def newMenu():
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        owner = getUserInfo(restaurant.user_id)
        if owner.id != login_session['user_id']:
            flash('You do not have access to edit %s.' % restaurant.name)
            return redirect(url_for('showRestaurants'))
        if request.method == 'POST':
            newItem = MenuItem(
            name = request.form['name'].strip(),
            description = request.form['description'].strip(),
            course = request.form['course'].strip(),
            price = request.form['price'].strip(),
            restaurant_id = restaurant.id)
            session.add(newItem)
            session.commit()
            flash('Menu item ' + '"' + newItem.name + '"' + ' created.')
            return redirect(url_for('showMenu', restaurant_id=restaurant_id))
        else:
            return render_template('_page.html', title='New Menu Item', view='newMenuItem', restaurant=restaurant)