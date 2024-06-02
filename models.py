from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import select
from sqlalchemy import Integer, String, BLOB, ForeignKey
from sqlalchemy.orm import mapped_column
import random



class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"

db.init_app(app)


class User(db.Model):
    id = mapped_column(Integer, primary_key=True,autoincrement=True)
    username = mapped_column(String(30), unique=True)
    email = mapped_column(String, unique=True)
    
    files = db.relationship("File", back_populates="user")

    def __repr__(self):
        return f"User({self.id}, {self.username}, {self.email})"

    def __init__(self, username, email):
        self.username = username
        self.email = email


class File(db.Model):
    id = mapped_column(Integer, primary_key=True,autoincrement=True)
    user_id = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    file = mapped_column(BLOB)

    user = db.relationship("User", back_populates="files")

    def __repr__(self):
        return f"File({self.id}, {self.user_id})"

    def __init__(self, user_id, file):
        self.user_id = user_id
        self.file = file



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        username = str(random.randbytes(10).hex())
        email = str(random.randbytes(10).hex())
        user = User(username, email)
        db.session.add(user)
        db.session.commit()
        print(user.id)
        file1 = File(user.id, random.randbytes(1000))
        file2 = File(user.id, random.randbytes(1000))
        db.session.add_all([file1,file2])
        db.session.commit()
        print([e for e in db.session.execute(select(User))])
