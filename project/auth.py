# auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from flask-security import current_user
from .models import User
from . import db
import os
import secrets
from PIL import Image
from datetime import datetime

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password): 
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():

    email = request.form.get('email')
    name = request.form.get('name') #--------------------------------------------------------- don't need
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again  
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@users_blueprint.route('/password_change', methods=["GET", "POST"])
@login_required
def ModifyPassword():
    form = PasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = current_user
            user.password = form.password.data
            db.session.add(user)  #-------------------------------------------------------------------------------
            db.session.commit()
            flash('Your password has been successfully changed!', 'success')
            return redirect(url_for('users.user_profile'))
    return render_template('password_change.html', form=form)

@app.route('/menu')
def showMenu():
    menuItems = session.query(MenuItem).filter_by(stock>0).all()
    if not menuItems:
        flash('There are currently no menu items for this restaurant.')

    return render_template('menu.html', title='Menu')



# The Admin page requires an 'Admin' role.
@app.route('/admin/new', methods=['GET', 'POST'])
@login_required
def updateProfile():
   
    
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.phonenumber = form.phonenumber.data
        current_user.adress = form.adress.data
        current_user.plateNum = form.plateNum.data
        current_user.carDescription = form.carDescription.data

        db.session.commit()
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.phonenumber.data = current_user.phonenumber
        form.adress.data = current_user.adress
        form.plateNum.data = current_user.plateNum
        form.carDescription.data = current_user.carDescription

    return render_template('profile.html', form=form)

def savePicture(picture):
    randomHex = secrets.token_hex(8)
    _, ext = os.path.splitext(picture.filename)
    pictureFinlname = randomHex + ext
    picturePath = os.path.join(app.root_path, 'static/menuPics', pictureFinlname)

    outputSize = (125, 125)
    i = Image.open(picture)
    i.thumbnail(outputSize)
    i.save(picturePath)

    return pictureFinlname

# The Admin page requires an 'Admin' role.
@app.route('/admin/new', methods=['GET', 'POST'])
@roles_required('Admin')    # Use of @roles_required decorator
@login_required
def addMenuItem():
    # if current_user.is_authenticated:
    #     return redirect(url_for('login'))

    # if current_user.role_id != 1:
    #     flash("You have no permission to modify menu")
    
    form = MenuForm()
    if form.validate_on_submit():  
        newItem = MenuItem(name = form.name.data,
                           price = form.price.data,
                           stock = form.stock.data,
                           category = form.category.data)
        if form.picture.data:
            pictureFile = save_picture(form.picture.data)
            newItem.picture = pictureFile
        db.session.add(newItem)
        db.session.commit()
        flash('Your menu item has been added!', 'success')
        return redirect(url_for('showMenu')
    return render_template('menu.html', form=form)


# The Admin page requires an 'Admin' role.        
@app.route('/admin/<int:post_menuItemID>/update', methods=['GET', 'POST'])
@roles_required('Admin')    # Use of @roles_required decorator
@login_required
def modifyMenuItem(menuItemID):
    # if current_user.is_authenticated:
    #     return redirect(url_for('login'))

    # if current_user.role_id != 1:
    #     flash("You have no permission to modify menu")
        
    menuItem = session.query(MenuItem).filter_by(id = menuItemID).one()
    form = MenuForm()
    if form.validate_on_submit():
        if form.picture.data:
            pictureFile = save_picture(form.picture.data)
            menuItem.picture = pictureFile
        menuItem.name = form.name.data
        menuItem.price = form.price.data
        menuItem.stock = form.stock.data
        menuItem.category = form.category.data
        db.session.commit()
        flash('Your menu has been updated!', 'success')
        return redirect(url_for('showMenu')

    elif request.method == 'GET':
        form.name.data =  menuItem.name
        form.price.data = menuItem.price
        form.stock.data = menuItem.stock
        form.category.data = menuItem.category
    return render_template('menu.html', form=form)

@app.route("/admin/<int:post_menuItemID>/delete", methods=['POST'])
@login_required
@roles_required('Admin')    # Use of @roles_required decorator
def deleteMenuItem(menuItemID):
    menuItem = session.query(MenuItem).filter_by(id = menuItemID).one()
    
    db.session.delete(menuItem)
    db.session.commit()
    flash('Your menu item has been deleted!', 'success')
    return redirect(url_for('menu.html'))

# create an order for an cunstomer
@app.route("/order/submit", , methods=['POST'])
@login_required
def create_order(food_dic): 
    cust_id = current_user.id
    order = Order(cust_id=cust_id)
    db.session.add(order)
    db.session.commit()
    
    total_price = 0
    for food_id, food_qty in food_dic.items():
        add = OrderItem(order_id=order.id, food_id=food_id, food_qty=food_qty)
        food_price = session.query(MenuItem).filter_by(id=food_id).one().price
        total_price += food_price*food_qty
        db.session.add(add)
        db.session.commit() 
    
    # update order table   
    order_form = OrderForm()
    pay_order = session.query(Order).filter_by(id == order_id).one().update({
                            'checkoutTime': datetime.now(), 
                            synchronize_session=False)
                                                                            
    # update customer payment method
    user_update = session.query(User).filter_by(id == cust_id)                                                                   
    
    if form.validate_on_submit():
        pay_order.pickup = form.pickup.data
        if form.pickup.data:
            pay_order.pickupTime = form.pickupTime.data
            user_update.plateNum = form.plateNum.data
            user_update.carDescription = form.carDescription.data
        
        pay_order.bill_amount = total_price
        uer_update.payment = form.payMethod.data
        db.session.commit()
        return redirect(url_for('showOrder')
    
    # form.pickup.data =  pay_order.pickup
    # form.pickupTime.data = pay_order.pickupTime
    # form.bill_amount.data = pay_order.bill_amount
    
    
    return render_template('order.html', form=form)
    
    
    # pay_order = session.query(Order).filter_by(Order.id == order_id).update({
    #                         'checkoutTime': datetime.now(), 
    #                         'pickup': pickup, 
    #                         'pickupTime': pickup_time,
    #                         'bill_amount': total_price}, 
    #                         synchronize_session=False)
    
# calculate the menu items' usage between a period    
def period_usage(self, d1, d2):
     
    usage = text("""SELECT menu_item.name, menu_item.stock, SUM(order_items.food_qty)
                   FROM menu_item, order, order_items
                   WHERE date(order.checkoutTime) BETWEEN :x AND :y
                   AND order.id = order_items.order_id
                   AND order_items.food_id = menu_item.id
                   GROUP BY menu_item.id
                   ORDER BY SUM(order_items.food_qty) DESC;""")
    result1 = session.connection().execute(usage, x=d1, y=d2).fetchall()
    return result
    
# calculate all menu items' usage between a period    
def period_total_usage(self, d1, d2):
     
    total_usage = text("""SELECT SUM(order_items.food_qty)
                   FROM  order, order_items
                   WHERE date(order.checkoutTime) BETWEEN :x AND :y
                   AND order.id = order_items.order_id;""")
    result2 = session.connection().execute( total_usage, x=d1, y=d2).fetchall()
    return result
    
# calculate the revenue between a period    
def period_revenue(self, d1, d2):
     
    revenue = text("""SELECT SUM(bill_amount)
                FROM order
                WHERE date(order.checkoutTime) BETWEEN :x AND :y;""")
    result = session.connection().execute(revenue,  x=d1, y=d2).fetchall()
    return result    



