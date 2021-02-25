# init.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import update
# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

@app.route('/customer/menu')
def viewMenu(user_id):
    # This page is the menu for restaurant viewed by customer
    if request.method == 'POST':
        menu = session.query(MenuItem).all()
        menu.name = request.form['name']
        menu.price = request.form['price']
        menu.description = request.form['description']
        menu.course = request.form['course']
        session.add(menu)
        session.commit()
        return render_template('viewMenu.html', user_id = user_id);



@app.route('/customer/createorder')
def createOrder(user_id):
    # This page is for making a new order for customer
    return render_template('createOrder.html')

@app.route('/customer/getreceipt')
def getReceipt(user_id):
    # This page is for making a new order for customer
    return render_template('getReceipt.html')

@app.route('/staff/editmenu')
@login_required
def editMenu(staff_id, menu_item_id):
    # This page is for staff updating menu items
    current_user = staff_id;
    if current_user.id != login_session['user_id']:
        flash('You do not have access to edit restaurant menu%s.')
        return redirect(url_for('LoginPage'))
    if request.method == 'POST':
        item.name = request.form['name'].strip()
        item.availability = request.form['availablity'].strip()
        session.add(item)
        session.commit()
        flash('The menu item availability' + '"' + item.name + '"' + ' has been updated.')
        return redirect(url_for('showMenu'))
    else:
         return render_template('_page.html', title='Edit Menu Item', view='editMenuItem', item=item)

@app.route('/staff/printorders')
def printOrders(staff_id):
    # This page is for staff printing orders
    # all orders
    return render_template('printOrders.html')

@app.route('/staff/prioritizeorders')
def prioritizeOrders(staff_id):
    # This page is for staff prioritizing orders for customer
    # boolean 
    # prioritized or not categorized (order id)
    return render_template('prioritizeOrders.html')

@app.route('/staff/markorders')
def markOrders(staff_id, order_id):
    # This page is for staff marking orders as complete
    current_user = staff_id;
    if current_user.id != login_session['user_id']:
        flash('You do not have access to edit customer orders%s.')
        return redirect(url_for('LoginPage'))
    if request.method == 'POST':
        current_user.order_id = session.query(order_id).one();
        if (order_id == current_user.order_id ):
            item.orderStatus = request.form['orderStatus'].strip();
        return render_template('markOrders.html')

    

