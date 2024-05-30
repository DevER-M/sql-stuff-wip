from flask import Flask, request, render_template
from backend import *

app = Flask(__name__)


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


if __name__ == "__main__":
    app.run()
