from fileshare import app, db
from sqlalchemy import select
from fileshare.forms import RegisterForm, LoginForm
from flask import render_template, session, redirect, flash
from fileshare import bcrypt
from fileshare.models import User, File


@app.route("/show_table/")
def showtable():
    u = select(User)
    allusers = db.session.execute(u).scalars().all()
    return str(allusers)


@app.route("/register", methods=["GET", "POST"])
def register():
    form: RegisterForm = RegisterForm()
    if form.validate_on_submit():
        salted_password = bcrypt.generate_password_hash(form.password.data)
        user = User(form.username.data, form.email.data, salted_password)
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    return render_template("signup.html", form=form)


@app.route("/home")
@app.route("/")
def root():
    try: 
        username = User.query.filter_by(email=session["email"]).first().username
    except: 
        username =  None
    return render_template("home.html",username=username)


@app.route("/login", methods=["GET", "POST"])
def login():
    form: LoginForm = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
            user.password, form.password.data
        ):
            session["email"] = user.email
            session["loggedin"] = True
            return redirect("/home")
        else:
            flash("make sure you enter the right email and password")
            redirect("/login")

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    session.pop("email")
    session.pop("loggedin", None)
    flash("logged out!", "info")
    return redirect("/home")

@app.route("/account")
def account():
    user = User.query.filter_by(email=session.get("email")).first()
    return render_template("account.html",user=user,username=user.username)
