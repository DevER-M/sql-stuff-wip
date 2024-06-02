from flask import Flask, request, render_template, session, redirect, flash
from backend import *
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


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
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        return new_user_login(username, password, connect("sql.db"))
    return render_template("signup.html")


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


if __name__ == "__main__":
    with connect("sql.db") as conn:
        cur = conn.cursor()
        create_files_table(cur)
        create_users_table(cur)
    app.run()
