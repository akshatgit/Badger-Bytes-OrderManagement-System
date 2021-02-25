from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User

class ProfileForm():
    name = StringField('Name',validators=[InputRequired(),Length(min=2, max=20)])
    phone = StringField('Phone Number',validators=[InputRequired(), ])
    adress = TextAreaField('Adress',validators=[InputRequired(), Length(max=200)])
    plateNum = StringField('Car Plate Num',validators=[InputRequired(),Length(min=2, max=20)])
    carDescription = TextAreaField('Car Description',validators=[InputRequired(), Length(max=500)])
    submit = SubmitField('Update')