from fileshare import app, db
from sqlalchemy import select
from fileshare.forms import RegisterForm, LoginForm
from flask import render_template, redirect, flash
from fileshare import bcrypt
from fileshare.models import User
from flask_login import login_user, logout_user, login_required, current_user


@app.route("/show_table/")
def showtable():
    u = select(User)
    allusers = db.session.execute(u).scalars().all()
    return str(allusers)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect("/home")
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
        username = (
            User.query.filter_by(email=session["email"]).first().username
        )
    except:
        username = None
    return render_template("home.html", username=username)


@app.route("/login", methods=["GET", "POST"])
def login():
    form: LoginForm = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
            user.password, form.password.data
        ):
            login_user(user, remember=True)
            flash("Logged in!")
            return redirect("/home")
        else:
            flash("make sure you enter the right email and password")
            redirect("/login")

    return render_template("login.html", form=form)


@login_required
@app.route("/logout")
def logout():
    logout_user()
    flash("Logged out!", "info")
    return redirect("/home")


@login_required
@app.route("/account")
def account():
    return render_template(
        "account.html",
    )
