from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo

class farmer_signup(FlaskForm):
    username = StringField('Name', validators=[DataRequired(), Length(min=2, max=15)], description="Username")
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=10), Regexp('^\d+$', message="Phone number must contain only digits")])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message='Too short')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message="Password must be Equal to Created password")])
    flat_no = StringField("flat_no", validators=[DataRequired(), Length(min=1, max=40)])
    street = StringField("Street", validators=[DataRequired(), Length(min=5, max=40)])
    town = StringField("Town", validators=[DataRequired(), Length(min=5, max=40)])
    state = StringField("State", validators=[DataRequired(), Length(min=4, max=30)])
    pincode = StringField("Pincode", validators=[DataRequired(), Length(min=6, max=6)])
    country = StringField("Country", validators=[DataRequired(), Length(min=5, max=40)])
    submit = SubmitField('SIGN UP')

class farmer_login(FlaskForm):
    username = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')