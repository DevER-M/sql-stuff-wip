import sqlite3
from utils import *
import bcrypt


class LoginInvalid(Exception):
    pass


def new_user_login(username: str, password: str, connection: sqlite3.Connection):
    """adds the user to user table"""
    with connection:
        cursor = connection.cursor()
        salted_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        if user_already_exists(cursor, username):
            return "username already exists try another one :("

        else:
            insert(
                "users",
                {"name": username, "password": salted_password},
                cursor,
            )
            return "Made an account :0"


def user_login(username: str, password: str, connection: sqlite3.Connection):
    with connection:
        cursor = connection.cursor()
        if user_already_exists(cursor, username):
            salted_password = password_from_db(cursor, username)
            if bcrypt.checkpw(password.encode(), salted_password):
                return True
            else:
                return LoginInvalid("Password Invalid")
        else:
            return LoginInvalid("Username does not exist")


def add_files_to_user(username: str, filepath: str, connection: sqlite3.Connection):
    """add file path to table"""
    with connection:
        cur = connection.cursor()
        select_in_db("id", "users", username, cur)
        user_id = cur.fetchone()
        if user_id:
            insert("files", {"user_id": user_id[0], "filepath": filepath}, cur)
            connection.commit()
            return "added file!"

        else:
            return "User not found!"


if __name__ == "__main__":
    with connect() as conn:
        c = conn.cursor()
        create_users_table(c)
        create_files_table(c)
        print(new_user_login("idk", "1234", conn))
        print(show_table(c, "users"))
        print(new_user_login("tuntun1234", "nicepassword", conn))
        print(user_login("sioj", "1234", conn))
