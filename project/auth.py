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

@auth.route('/settingspage')
@login_required
def settingspage():
    return render_template('settings.html')


@auth.route('/settings',  methods=['GET', 'POST'])
@login_required
def settings():
    form = ProfileForm()
    if request.method == "POST":
        # current_user.name = form.name.data
        # current_user.phone = form.phone.data
        # current_user.address = form.address.data
        # current_user.plateNum = form.plateNum.data
        # current_user.carDescription = form.carDescription.data
        # current_user.password = generate_password_hash(form.password.data, method='sha256')
        current_user.name = request.form["name"]
        current_user.phone = request.form["phone"]
        current_user.address = request.form["address"]
        current_user.password = generate_password_hash(request.form["password"], method='sha256')
        current_user.plateNum = request.form["plateNum"]
        current_user.carDescription = request.form["carDescription"]
       
        db.session.commit()
    # else:
    #     form.name.data = current_user.name
    #     form.phone.data = current_user.phone
    #     form.address.data = current_user.address
    #     form.plateNum.data = current_user.plateNum
    #     form.carDescription.data = current_user.carDescription      
    return render_template('profile.html', name=current_user.name, form=form)

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
    name = request.form.get('name')
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