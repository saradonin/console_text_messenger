from psycopg2 import connect, OperationalError
from psycopg2.errors import DuplicateDatabase, DuplicateTable

DB_USER = "postgres"
DB_PASSWORD = "coderslab"
DB_HOST = "localhost"

CREATE_DB = "CREATE DATABASE workshop;"

CREATE_USERS_TABLE = """CREATE TABLE users (
    id serial PRIMARY KEY, 
    username varchar(255) UNIQUE,
    hashed_password varchar(80));"""

CREATE_MESSAGES_TABLE = """CREATE TABLE messages (
    id serial PRIMARY KEY, 
    from_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    to_id INTEGER REFERENCES users(id) ON DELETE CASCADE, 
    text varchar(255),
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"""


def create_table(sql_query):
    try:
        cursor.execute(sql_query)
        print("Table created")
    except DuplicateTable as e:
        print("Table exists: ", e)


def create_database(sql_query):
    try:
        cursor.execute(sql_query)
        print("Database created")
    except DuplicateDatabase as e:
        print("Database exists: ", e)


try:
    cnx = connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
    cnx.autocommit = True
    cursor = cnx.cursor()

    create_database(CREATE_DB)

    cnx.close()
except OperationalError as e:
    print("Connection Error: ", e)

try:
    cnx = connect(database="workshop", user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
    cnx.autocommit = True
    cursor = cnx.cursor()

    create_table(CREATE_USERS_TABLE)
    create_table(CREATE_MESSAGES_TABLE)

    cnx.close()
except OperationalError as e:
    print("Connection Error: ", e)
