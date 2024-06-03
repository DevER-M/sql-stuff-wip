from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import DeclarativeBase
from flask_bootstrap import Bootstrap


class Base(DeclarativeBase):
    pass


app = Flask(__name__)
db = SQLAlchemy(model_class=Base)
bcrypt = Bcrypt(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "iuhe398h432u8hnf401fhni32"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sql.db"

db.init_app(app)
Session(app)
Bootstrap(app)

with app.app_context():
    db.create_all()

from fileshare import routes
