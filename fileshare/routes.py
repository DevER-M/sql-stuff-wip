from . import app
from forms import RegisterForm
from flask import request, render_template, session, redirect, flash
from utils import show_table,create_table,connect
from backend import (
    new_user_login,
    user_login,
    LoginInvalid,
)

@app.route("/show_table/<table>")
def showtable(table: str):
    temp_cursor = connect("sql.db").cursor()
    return str(show_table(temp_cursor, table))


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
        return new_user_login(form.username.data, form.password.data, connect("sql.db"))
    return render_template("signup.html", form=form)


@app.route("/")
def root():
    if not session.get("username"):
        return redirect("/login")
    return f"hi {session["username"]}"


@app.route("/login", methods=["GET", "POST"])
def login():
    with connect("sql.db") as conn:
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            try:
                user_login(username, password, conn)
                session["username"] = username
                session["logged_in"] = True
                return "logged in nice"
            except LoginInvalid as e:
                return str(e)
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("username")
    session.pop("logged_in", None)
    flash("logged out!", "info")
    return redirect("/login")
