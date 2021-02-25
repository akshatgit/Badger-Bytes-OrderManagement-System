from flask-security import current_user, login_required
@server.route('customer/profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    userform = ProfileForm()
    # Modify and update profile
    if userform.validate_on_submit():
        current_user.firstname = userform.firstname.data
        current_user.lastname = userform.lastname.data
        current_user.phonenumber = userform.phonenumber.data
        current_user.address = userform.address.data
        db.session.commit()
        flash('Your Profile Has Been Updated')
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.phonenumber.data = current_user.phonenumber
        form.address.data = current_user.address

   
    return render_template('profile.html', form=userform) 