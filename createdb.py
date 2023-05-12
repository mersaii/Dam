# from app import engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from flask_login import UserMixin
from datetime import datetime
from flask import Flask
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
conn_string = "sqlite:///"+os.path.join(BASE_DIR,'database.db')
app.config['SECRET_KEY'] = 'ausefulkeys'
Base = declarative_base()
engine = create_engine(conn_string, echo=True)

Session = sessionmaker()
local_session = Session(bind=engine)


class User(Base, SQLAlchemy, UserMixin):
    __tablename__ = 'users'
    
    id = Column(Integer(), autoincrement=True, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(), nullable=False,unique=True)
    password = Column(String(80), nullable=False)
    datecreated = Column(DateTime(), default=datetime.utcnow)
    
    def __repr__(self):
        return f'username: {self.username}, email: {self.email}'


Base.metadata.create_all(engine)