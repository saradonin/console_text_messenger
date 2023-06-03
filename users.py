import argparse

from psycopg2 import connect, OperationalError
from psycopg2.errors import UniqueViolation

from clcrypto import check_password
from models import User


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-n", "--new_pass", help="new password (min 8 characters)")
parser.add_argument("-l", "--list", help="list all users", action="store_true")
parser.add_argument("-d", "--delete", help="delete user", action="store_true")
parser.add_argument("-e", "--edit", help="edit user", action="store_true")

args = parser.parse_args()





def create_user(cur, username, password):
    if len(password) < 8:
        print("Password is tho short. It should have minimum 8 characters.")
    else:
        try:
            user = User(username=username, password=password)
            user.save_to_db(cur)
            print("User created")
        except UniqueViolation as e:
            print("User already exists. ", e)


def list_users(cur):
    users = User.load_all_users(cur)
    for user in users:
        print(user.username)


