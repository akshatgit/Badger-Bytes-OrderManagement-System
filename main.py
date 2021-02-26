# main.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask import session as login_session

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@users_blueprint.route('/account', methods=["GET", "POST"])
@login_required
def account():

    form = UpdateAccountForm()

    if form.validate_on_submit():

        current_user.username = form.username.data
        db.session.commit()
        flash('Your username has been updated ', 'success')
        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.username.data = current_user.username

    return render_template('account.html', form=form)

