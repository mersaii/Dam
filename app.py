from flask import Flask, render_template, url_for, redirect
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from flask_bcrypt import Bcrypt
from forms import *
from createdb import *
import os
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
conn_string = "sqlite:///"+os.path.join(BASE_DIR,'database.db')
app.config['SECRET_KEY'] = 'ausefulkeys'
Base = declarative_base()
engine = create_engine(conn_string, echo=True)

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

Session = sessionmaker()
local_session = Session(bind=engine)

@login_manager.user_loader
def load_user(user_id):
    return local_session.query(User).get(int(user_id))

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')
    
@app.route('/login', methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = local_session.query(User).filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('login'))
    return render_template('login.html', form=form)
    

@app.route('/signup', methods = ['GET','POST'])
def signup():
    form = RegisterForm()
    
    if form.validate_on_submit():
        hashed_p = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_p, email=form.email.data )
        local_session.add(new_user)
        local_session.commit()
        return redirect(url_for('login'))  
    return render_template('signup.html', form=form)
    
@app.route('/dashboard', methods = ['GET'])
@login_required 
def dashboard():
    form = LoginForm()
    
    return render_template('dashboard.html', form=form)


@app.route('/logout', methods = ['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
    
if __name__ == '__main__':
    app.run(debug=True)
    
    
    
    
    




# from flask_login import UserMixin
# from datetime import datetime
# from wtforms import StringField, PasswordField, SubmitField, EmailField
# from wtforms.validators import InputRequired, Length, ValidationError
# from flask_wtf import FlaskForm
# from flask_sqlalchemy import SQLAlchemy
# from flask import Flask, render_template, url_for, redirect
# from sqlalchemy.orm import declarative_base, sessionmaker
# from sqlalchemy import create_engine #Column, Integer, String, DateTime
# from flask_bcrypt import Bcrypt
# from forms import *
# from createdb import *
# import os

    
    
# @app.route('/careers', methods = ['GET'])
# def careers():
#     return render_template('careers.html')

# @app.route('/eachcareer', methods =['GET'])
# def eachcareer():
#     return render_template('eachcareer.html')