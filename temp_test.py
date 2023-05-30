from psycopg2 import connect, OperationalError
from models import User

DB_USER = "postgres"
DB_PASSWORD = "coderslab"
DB_HOST = "localhost"

cnx = connect(database="workshop", user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
cnx.autocommit = True
cursor = cnx.cursor()


user1 = User('medeh', 'haslo123')
user1.save_to_db(cursor)
