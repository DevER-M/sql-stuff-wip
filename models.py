from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import Column, Integer, Text, ForeignKey, BLOB
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(20)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sql.db"
db = SQLAlchemy(app)
Base = declarative_base()


class User(db.Model):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    password = Column(BLOB, nullable=False)

    # Relationship to files
    files = relationship("File", back_populates="user")

    def __repr__(self):
        return f"User({self.id}, {self.name})"


class File(db.Model):
    __tablename__ = "file"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_content = Column(BLOB, nullable=False)

    # Relationship to user
    user = relationship("User", back_populates="files")

    def __repr__(self):
        return f"File({self.id}, {self.user_id})"
    


with app.app_context():
    db.create_all()
    user1 = User()
    user1.name="aname"
    
    
    db.session.add(user1)
    db.session.commit()
