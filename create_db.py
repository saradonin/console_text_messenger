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


def execute_sql(sql_query):
    if 'CREATE DATABASE' in sql_query:
        msg = 'Database created.'
    elif 'CREATE TABLE' in sql_query:
        msg = 'Table created'
    else:
        msg = 'SQL query executed'

    try:
        cursor.execute(sql_query)
        print(msg)
    except DuplicateDatabase as e:
        print("Database exists: ", e)
    except DuplicateTable as e:
        print("Table exists: ", e)


try:
    cnx = connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
    cnx.autocommit = True
    cursor = cnx.cursor()

    execute_sql(CREATE_DB)

    cnx.close()
except OperationalError as e:
    print("Connection Error: ", e)

try:
    cnx = connect(database="workshop", user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
    cnx.autocommit = True
    cursor = cnx.cursor()

    execute_sql(CREATE_USERS_TABLE)
    execute_sql(CREATE_MESSAGES_TABLE)

    cnx.close()
except OperationalError as e:
    print("Connection Error: ", e)
