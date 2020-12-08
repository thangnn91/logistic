from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, IntegerField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    email = StringField('Email', validators=[DataRequired(), Email(message=('Email không đúng định dạng'))])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message=('Email không đúng định dạng'))])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')
    
class ChangepassForm(FlaskForm):
    old_pass = PasswordField('oldpass', validators=[DataRequired()])
    new_pass = PasswordField('newpass', validators=[DataRequired()])
    submit = SubmitField('Changepass')
    
class CreateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message=('Email không đúng định dạng'))])
    password = PasswordField('Password', validators=[DataRequired()])
    usertype = IntegerField('UserType')
    mobile = StringField('Email')
    submit = SubmitField('CreateUser')