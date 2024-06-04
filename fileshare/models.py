from fileshare import db, login_manager
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String, BLOB, ForeignKey
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    username = mapped_column(String(30), unique=True)
    email = mapped_column(String, unique=True)
    password = mapped_column(BLOB, nullable=False)

    files = db.relationship("File", back_populates="user")

    def __repr__(self):
        return f"User({self.id}, {self.username}, {self.email})"

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


class File(db.Model):
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    file = mapped_column(BLOB)

    user = db.relationship("User", back_populates="files")

    def __repr__(self):
        return f"File({self.id}, {self.user_id})"

    def __init__(self, user_id, file):
        self.user_id = user_id
        self.file = file
