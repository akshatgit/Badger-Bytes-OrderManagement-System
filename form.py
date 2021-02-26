from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, SelectField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError


class CustOrderForm(FlaskForm):
    payMethod = SelectField('Pay Method', choices=[('PayPal', 'PayPal'), ('ApplePay', 'ApplePay'), ('Stripe', 'Stripe')])
    plateNum = StringField('Car Plate Num',validators=[InputRequired(),Length(min=2, max=20)])
    carDescription = TextAreaField('Car Description',validators=[InputRequired(), Length(max=500)])
    