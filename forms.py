from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_wtf import FlaskForm
from createdb import *


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'username'})
    email = EmailField(validators=[InputRequired(), Length(min=4, max=30)], render_kw={'placeholder': 'email'})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20), ], render_kw={'placeholder': 'password'})
    submit = SubmitField('Register')
    
    # def validate_username(self,username):
    #     existing_user = local_session.query(User).filter_by(username=username.data).first()
    #     if existing_user:
    #         raise ValidationError('Username already exists. Please choose a different one')
        
    # def validate_email(self, email):
    #     existing_email = local_session.query(User).filter_by(email = email.data).first()
    #     if existing_email:
    #         raise ValidationError('Email already exists. Please choose a different one')
            
        
    # def validate(self, extra_validators=None):
    #     return super().validate(extra_validators)

class LoginForm(FlaskForm):
    # username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'username'})
    email = EmailField(validators=[InputRequired(), Length(min=4, max=30)], render_kw={'placeholder': 'email'})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'password'})
    submit = SubmitField('Login')