# auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from models import User
from server import db


auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/settings', methods=["GET", "POST"])
@login_required
def settings(): 
    if request.method == 'POST':
        print(request.form)
        user = User.query.filter_by(email=current_user.email).first()

        user.name = request.form.get('name')
        user.phone = request.form.get('Phone Number')
        user.address = request.form.get('address')
        user.password = generate_password_hash(request.form.get('password'),method='sha256')
        user.payment = request.form.get('payment')
        db.session.commit()
        return redirect(url_for('main.profile'))
    else:
        return render_template('settings.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('usertype')
    print(role)
    # print(request.form)
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password) or role != user.role: 
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
    name = request.form.get('name')
    password = request.form.get('password')
    role = request.form.get('User')
    address = request.form.get('Address')
    phone = request.form.get('Phone Number')
    payment = request.form.get('payment')
    print(request.form)
    print(role)
    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again  
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, name=name, role = role, password=generate_password_hash(password, method='sha256'),
                address = address,
                phone = phone
                )

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))