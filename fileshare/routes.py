import bcrypt
from fileshare import app,db
from sqlalchemy import select
from fileshare.forms import RegisterForm,LoginForm
from flask import render_template, session, redirect, flash
from fileshare.utils import show_table,create_table,connect
from fileshare.models import User,File

@app.route("/show_table/")
def showtable():
    u = select(User)
    allusers = [e for e in db.session.execute(u).scalars().all()]
    return allusers



@app.route("/create_table/<tablename>")
def newtable(tablename: str):
    temp_cursor = connect("sql.db").cursor()
    result = create_table(tablename, temp_cursor)
    print(result)
    if result:
        return str(show_table(temp_cursor, tablename))
    else:
        return result


@app.route("/register", methods=["GET", "POST"])
def register():
    form: RegisterForm = RegisterForm()
    if form.validate_on_submit():
        salted_password = bcrypt.hashpw(str(form.password.data).encode(), bcrypt.gensalt())
        user = User(form.username.data,form.email.data,salted_password)
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    return render_template("signup.html", form=form)


@app.route("/")
def root():
    if not session.get("email"):
        return redirect("/login")
    return f"hi {session["email"]}"


@app.route("/login", methods=["GET", "POST"])
def login():
    form:LoginForm = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.checkpw(user.password,form.password.data):
            redirect("/")

    return render_template("login.html",form=form)


@app.route("/logout")
def logout():
    session.pop("email")
    session.pop("loggedin", None)
    flash("logged out!", "info")
    return redirect("/login")
