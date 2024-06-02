from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"

db.init_app(app)


from sqlalchemy import Integer, String,BLOB,ForeignKey
from sqlalchemy.orm import mapped_column

class User(db.Model):
    id = mapped_column(Integer,primary_key=True)
    username = mapped_column(String(30),unique=True)
    email = mapped_column(String,unique=True)

    def __init__(self,username,email):
       self.username = username
       self.email = email

class Files(db.Model):
    id = mapped_column(Integer,primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"),unique=True)
    file = mapped_column(BLOB,unique=True)

    def __init__(self,username,email):
       self.username = username
       self.email = email

import random
with app.app_context():
    db.create_all()
    user = User(username=str(random.randbytes(10).hex()),email=str(random.randbytes(10).hex()))
    db.session.add(user)
    db.session.commit()

