USER = 'postgres'
PASSWORD = 'coderslab'
HOST = 'localhost'

CREATE_DB = """CREATE DATABASE workshop;"""

CREATE_USERS_TABLE = """
CREATE TABLE users (
id serial PRIMARY KEY,
username varchar(255) UNIQUE,
hashed_passwors varchar(80)
);
"""

CREATE_MESSAGES_TABLE = """
CREATE TABLE messages (
id serial PRIMARY KEY,
from_id int REFERENCES users(id) ON DELETE CASCADE,
to_id int REFERENCES users(id) ON DELETE CASCADE,
creation_date TIMESTAMP DEFAULT current_timestamp,
text varchar(255)
);
"""

