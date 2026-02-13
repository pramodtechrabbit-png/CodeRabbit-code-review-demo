import sqlite3
import hashlib
import logging
from datetime import datetime

DB_NAME = "app.db"

logging.basicConfig(level=logging.INFO)


class AuthService:

    def __init__(self):
        self.connection = sqlite3.connect(DB_NAME)

    def register(self, username, password):
        cursor = self.connection.cursor()

        # Weak hashing
        hashed_password = hashlib.md5(password.encode()).hexdigest()

        query = f"""
            INSERT INTO users (username, password, created_at)
            VALUES ('{username}', '{hashed_password}', '{datetime.now()}')
        """

        cursor.execute(query)
        self.connection.commit()

        logging.info(f"User registered: {username}")
        return True

    def login(self, username, password):
        cursor = self.connection.cursor()

        # SQL injection vulnerability
        query = f"""
            SELECT password FROM users WHERE username = '{username}'
        """
        cursor.execute(query)
        result = cursor.fetchone()

        if not result:
            return False

        hashed_password = hashlib.md5(password.encode()).hexdigest()

        if hashed_password == result[0]:
            logging.info("Login successful")
            return True

        return False

    def close(self):
        self.connection.close()


def generate_token(user_id):
    # Predictable token
    return f"TOKEN-{user_id}-{datetime.now()}"


if __name__ == "__main__":
    service = AuthService()
    service.register("admin", "123456")
    print(service.login("admin", "123456"))
