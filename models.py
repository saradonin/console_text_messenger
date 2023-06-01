from clcrypto import hash_password


class User:
    """
    Represents a user.

    :ivar _id: The user ID.
    :ivar username: The username of the user.
    :ivar _hashed_password: The hashed password of the user.
    """

    def __init__(self, username="", password="", salt=""):
        """
        Initialize a User object.

        :param username: The username of the user.
        :param password: The password of the user.
        :param salt: The salt value used for password hashing.
        """
        self._id = -1
        self.username = username
        self._hashed_password = hash_password(password, salt)

    @property
    def id(self):
        """
        Get the user's ID.

        :return: int: The user's ID.
        """
        return self._id

    @property
    def hashed_password(self):
        """
        Get the hashed password of the user.

        :return: str: The hashed password.
        """
        return self._hashed_password

    def set_password(self, password, salt=""):
        """
        Set the hashed password for the user.

        :param password: str - The new password to set.
        :param salt: str - The salt used for password hashing.
        """
        self._hashed_password = hash_password(password, salt)

    @hashed_password.setter
    def hashed_password(self, password):
        """
        Set the hashed password for the user.

        :param password: str - The new hashed password.
        """
        self.set_password(password)

    def save_to_db(self, cursor):
        """
        Save the user object to the database.

        :param cursor: The database cursor object.
        :return: True if the save operation is successful, False otherwise.
        """
        if self._id == -1:
            sql = """INSERT INTO users(username, hashed_password)
                            VALUES(%s, %s) RETURNING id"""
            values = (self.username, self.hashed_password)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]  # or cursor.fetchone()['id']
            return True
        else:
            sql = """UPDATE Users SET username=%s, hashed_password=%s
                           WHERE id=%s"""
            values = (self.username, self.hashed_password, self.id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_user_by_id(cursor, id_):
        """
        Load a user from the database by user ID.

        :param cursor: The database cursor object.
        :param id_: The user ID to load.
        :return: The loaded User object if found, None otherwise.
        """
        sql = "SELECT id, username, hashed_password FROM users WHERE id=%s"
        cursor.execute(sql, (id_,))  # (id_, ) - cause we need a tuple
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user

    @staticmethod
    def load_all_users(cursor):
        """
        Load all users from the database.

        :param cursor: The database cursor object.
        :return: A list of User objects.
        """
        sql = "SELECT id, username, hashed_password FROM Users"
        users = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, username, hashed_password = row
            loaded_user = User()
            loaded_user._id = id_
            loaded_user.username = username
            loaded_user._hashed_password = hashed_password
            users.append(loaded_user)
        return users

    def delete(self, cursor):
        """
        Delete the user from the database.

        :param cursor: The database cursor object.
        :return: True if the delete operation is successful, False otherwise.
        """
        sql = "DELETE FROM Users WHERE id=%s"
        cursor.execute(sql, (self.id,))
        self._id = -1
        return True


class Message:
    """
    Represents a message.

    :ivar _id: The message ID.
    :ivar from_id: The ID of the sender.
    :ivar to_id: The ID of the recipient.
    :ivar text: The content of the message.
    :ivar _creation_date: The creation date of the message.
    """

    def __init__(self, from_id, to_id, text):
        """
        Initialize a Message object.

        :param from_id: The sender's ID.
        :param to_id: The recipient's ID.
        :param text: The content of the message.
        """
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self._creation_date = None

    @property
    def creation_date(self):
        """
        Get the creation date of the message.

        :return: The creation date.
        """
        return self._creation_date

    @property
    def id(self):
        """
        Get the message ID.

        :return: The message ID.
        """
        return self._id

    def save_to_db(self, cursor):
        """
        Save the message object to the database.

        :param cursor: The database cursor object.
        :return: True if the save operation is successful, False otherwise.
        """
        if self._id == -1:
            sql = """INSERT INTO Messages(from_id, to_id, text)
                            VALUES(%s, %s, %s) RETURNING id, creation_date"""
            values = (self.from_id, self.to_id, self.text)
            cursor.execute(sql, values)
            self._id, self._creation_date = cursor.fetchone()
            return True
        else:
            sql = """UPDATE Messages SET to_id=%s, from_id=%s, text=%s WHERE id=%s"""
            values = (self.from_id, self.to_id, self.text, self.id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_all_messages(cursor, user_id=None):
        """
        Load all messages from the database.

        :param cursor: The database cursor object.
        :param user_id: (Optional) The ID of the user to filter messages by recipient.
        :return: A list of Message objects.
        """
        if user_id:
            sql = "SELECT id, from_id, to_id, text, creation_date FROM messages WHERE to_id=%s"
            cursor.execute(sql, (user_id,))  # (user_id, ) - cause we need a tuple
        else:
            sql = "SELECT id, from_id, to_id, text, creation_date FROM messages"
            cursor.execute(sql)
        messages = []
        for row in cursor.fetchall():
            id_, from_id, to_id, text, creation_date = row
            loaded_message = Message(from_id, to_id, text)
            loaded_message._id = id_
            loaded_message._creation_date = creation_date
            messages.append(loaded_message)
        return messages
