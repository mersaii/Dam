from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from flask_login import UserMixin
from datetime import datetime
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_wtf import FlaskForm
from flask_bcrypt import Bcrypt
import os


#creates instance of flask
app = Flask(__name__)

#holds path of cwd
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
app.config['SECRET_KEY'] = 'ausefulkeys'

#connects to database, shows which database to be used
conn_string = "sqlite:///"+os.path.join(BASE_DIR,'database.db')
bcrypt = Bcrypt(app)
#map table related to class create an instance of declarative base.
Base = declarative_base()

engine = create_engine(conn_string, echo=True)

Session = sessionmaker()

local_session = Session(bind=engine)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer(), autoincrement=True, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(), nullable=False,unique=True)
    password = Column(String(80), nullable=False)
    datecreated = Column(DateTime(), default=datetime.utcnow)
    
    def __repr__(self):
        return f'username: {self.username}, email: {self.email}'


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'username'})
    email = EmailField(validators=[InputRequired(), Length(min=4, max=30)], render_kw={'placeholder': 'email'})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'password'})
    submit = SubmitField('Register')
    
    def validate_username(self,username):
        existing_user = local_session.query(User).filter_by(username=username.data).first()
        if existing_user:
            raise ValidationError('Username already exists. Please choose a different one')
        
    def validate_email(self, email):
        existing_email = local_session.query(User).filter_by(email = email.data).first()
        if existing_email:
            raise ValidationError('Email already exists. Please choose a different one')
            
        
    # def validate(self, extra_validators=None):
    #     return super().validate(extra_validators)

class LoginForm(FlaskForm):
    # username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'username'})
    email = EmailField(validators=[InputRequired(), Length(min=4, max=30)], render_kw={'placeholder': 'email'})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'password'})
    submit = SubmitField('Login')

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')
    
@app.route('/login', methods = ['GET','POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)
 

@app.route('/signup', methods = ['GET','POST'])
def signup():
    form = RegisterForm()
    
    if form.validate_on_submit():
        hashed_p = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_p, email=form.email.data )
        local_session.add(new_user)
        local_session.commit()
        # try:
        #     local_session.commit()
        # except:
        #     local_session.rollback()
        #     print("Error: User already exists")
        #     raise
        return redirect(url_for('login'))  
    return render_template('signup.html', form=form)
    


 
@app.route('/careers', methods = ['GET'])
def careers():
    return render_template('careers.html')

@app.route('/eachcareer', methods =['GET'])
def eachcareer():
    return render_template('eachcareer.html')

 
 
 
 
 
 
 
 
 
 
 
    
if __name__ == '__main__':
    app.run(debug=True)