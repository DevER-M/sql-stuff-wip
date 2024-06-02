from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import select


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"

db.init_app(app)


from sqlalchemy import Integer, String, BLOB, ForeignKey
from sqlalchemy.orm import mapped_column


class User(db.Model):
    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String(30), unique=True)
    email = mapped_column(String, unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return f"User(id: {self.id},username: {self.username},email: {self.email})"


class File(db.Model):
    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"), unique=True)
    file = mapped_column(BLOB, unique=True)

    def __init__(self, user_id, file):
        self.user_id = user_id
        self.file = file

    def __repr__(self):
        return f"File(id: {self.id},user_id: {self.user_id})"


import random

with app.app_context():
    db.create_all()
    username = str(random.randbytes(10).hex())
    email = str(random.randbytes(10).hex())
    user = User(username, email)
    file = File(user.id, random.randbytes(1000))
    db.session.add_all([user, file])
    db.session.commit()
    print(db.session.execute(select(User)))
