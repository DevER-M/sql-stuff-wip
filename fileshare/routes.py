from fileshare import app, db
from sqlalchemy import select
from fileshare.forms import RegisterForm, LoginForm, AddFileForm
from flask import render_template, redirect, flash, request, send_file
from fileshare import bcrypt
from fileshare.models import User, File
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, login_required, current_user
from io import BytesIO


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
    if current_user.is_authenticated:
        files = File.query.filter_by(user_id=current_user.id).all()
        return render_template("home.html", files=files)
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form: LoginForm = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
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


@login_required
@app.route("/upload", methods=["GET", "POST"])
def upload():
    form: AddFileForm = AddFileForm()
    if request.method == "POST" and current_user.is_authenticated:
        file = form.file.data
        user_file = File(current_user.id, request.files["file"].read(), file.filename)
        db.session.add(user_file)
        db.session.commit()
        flash("done")
        return redirect("/upload")
    elif not current_user.is_authenticated:
        flash("Please login/register to upload files!")
        return render_template("upload.html", form=form)
    else:
        return render_template("upload.html", form=form)


@app.route("/download/<file_id>")
def download(file_id):
    file = File.query.filter_by(id=file_id).first()
    if current_user.is_authenticated and current_user.id == file.user_id:
        return send_file(BytesIO(file.file), download_name=file.filename)
    else:
        flash("File owner is different!")
        return redirect("/home")
