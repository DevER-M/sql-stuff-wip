import sqlite3
from hashlib import sha256


def connect(file=":memory:"):
    """connects to sql.db file"""
    return sqlite3.connect(file)


def create_users_table(cursor: sqlite3.Cursor):
    cursor.execute(
        """create table if not exists users (
               		 id integer primary key autoincrement,
                  	 name text,
                  	 password blob);
            """
    )


def create_files_table(cursor: sqlite3.Cursor):
    cursor.execute(
        """create table if not exists files (
                id integer primary key AUTOINCREMENT,
                user_id integer,
                filepath text,
                foreign key (user_id) references users(id)
            );"""
    )

def create_table(name:str,cursor:sqlite3.Cursor):
    try:
        cursor.execute(f"""create table if not exists {name} (
                id integer primary key AUTOINCREMENT,
                user_id integer,
                filepath text,
                foreign key (user_id) references users(id)
            );""")
        return True
    except Exception as e:
        return e
    

def hash(string: str):
    """hashes string to sha256 and returns hexdigest"""
    return sha256(string.encode()).hexdigest()


def all_tables_in_db(cursor: sqlite3.Cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    return [row[0] for row in cursor.fetchall()]


def all_columns_in_table(table: str, cursor: sqlite3.Cursor):
    cursor.execute(f"PRAGMA table_info({table})")
    columns_info = cursor.fetchall()
    return [column[1] for column in columns_info]


def show_table(cursor: sqlite3.Cursor, table: str):
    if table in all_tables_in_db(cursor):
        cursor.execute(f"select * from {table}")
        return cursor.fetchall()
    else:
        return None


def user_already_exists(cursor: sqlite3.Cursor, hashed_username: str):
    cursor.execute("select name from users where name=?", (hashed_username,))
    return cursor.fetchone() is not None


def password_from_db(cursor: sqlite3.Cursor, username: str):
    hashed_username = hash(username)
    cursor.execute("SELECT password FROM users WHERE name=?", (hashed_username,))
    result = cursor.fetchone()
    return bytes(result[0]) if result else b""


def insert(table: str, data: dict, cursor: sqlite3.Cursor):
    """Insert data into the specified table"""
    columns = ", ".join(data.keys())
    placeholders = ", ".join(["?"] * len(data))
    values = tuple(data.values())
    sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    cursor.execute(sql, values)


def select_in_db(column: str, table: str, name: str, cursor: sqlite3.Cursor):
    if table in all_tables_in_db(cursor) and column in all_columns_in_table(
        table, cursor
    ):
        cursor.execute(f"select {column} from {table} where name=?", (name,))
    else:
        return None
