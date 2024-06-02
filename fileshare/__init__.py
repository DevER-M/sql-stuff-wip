from flask_session import Session
from forms import LoginForm, RegisterForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask import Flask


class Base(DeclarativeBase):
    pass


app = Flask(__name__)
db = SQLAlchemy(model_class=Base)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "iuhe398h432u8hnf401fhni32"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db.init_app(app)
Session(app)
