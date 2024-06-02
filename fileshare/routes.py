from fileshare import app
from fileshare.forms import RegisterForm,LoginForm
from flask import render_template, session, redirect, flash
from fileshare.utils import show_table,create_table,connect
from fileshare.backend import (
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
    if not session.get("email"):
        return redirect("/login")
    return f"hi {session["username"]}"


@app.route("/login", methods=["GET", "POST"])
def login():
    form:LoginForm = LoginForm()
    if form.validate_on_submit():
        try:
            user_login(form.email.data,form.password.data,connect("sql.db"))
            session["loggedin"] = True
            session["email"] = form.email.data
        except LoginInvalid as e:
            return str(e)

    return render_template("login.html",form=form)


@app.route("/logout")
def logout():
    session.pop("username")
    session.pop("logged_in", None)
    flash("logged out!", "info")
    return redirect("/login")
