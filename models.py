from clcrypto import hash_password

class User:
    def __init__(self,username, password, salt):
        self._id = -1
        self.username = username
        self._hashed_password = hash_password(password, salt)


