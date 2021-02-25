from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User

class UpdateAccountForm():
    username = StringField('Username', validators=[InputRequired()])
    submit = SubmitField('Update')
    def validate_username(self, usrename):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose another one')

class UpdateProfileForm():
    firstname = StringField('First Name',validators=[InputRequired(),Length(min=2, max=20)])
    lastname = StringField('Last Name',validators=[InputRequired(),Length(min=2, max=20)])
    phonenumber = StringField('Phone Number',validators=[InputRequired(), ])
    adress = TextAreaField('Adress',validators=[InputRequired(), Length(max=200)])
    submit = SubmitField('Update')
    
class MenuForm(FlaskForm):
    name = StringField('Name',validators=[InputRequired(),Length(min=2, max=30)])
    price = DecimalField('Price',validators=[InputRequired(),Length(min=2, max=20)])
    stock = IntegerField('Stock', validators=[InputRequired()])
    picture = FileField('Update Menu Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

