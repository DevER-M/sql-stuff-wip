from fileshare.utils import *
from fileshare.backend import *
import random

with connect() as conn:
    cur = conn.cursor()
    create_users_table(cur)
    create_files_table(cur)
    username = str(random.randbytes(10).hex())
    password = str(random.randbytes(10).hex())
    file_path_random_text = str(random.randbytes(20).hex())
    print(
        f"""
username: {username}
password: {password}
random file path text: {file_path_random_text}
---------------------------------------------------------------"""
    )
    print(new_user_login(username, password, conn))
    print(show_table(cur, "users"))
    print(user_login(username, password, conn))
    print(add_files_to_user(username, file_path_random_text, conn))
    print(show_table(cur, "files"))
