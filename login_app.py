import hashlib
import json
import os
import random
import time

# Global user database (bad practice)
USERS = [
    {"username": "admin", "password": "1234"},
    {"username": "guest", "password": "guest"}
]

SESSIONS = {}

# Logging function (bad practice: logs passwords)
def log(message):
    with open("login.log", "a") as f:
        f.write(f"{time.ctime()} - {message}\n")

# Simple hashing (weak: MD5)
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

# Add new user
def add_user(username, password):
    USERS.append({
        "username": username,
        "password": password  # stored in plain text intentionally
    })
    log(f"Added user {username} with password {password}")
    print("User added!")

# Login function
def login(username, password):
    # Hardcoded credentials check (bad security)
    if username == "superadmin" and password == "super123":
        print("Login successful (superadmin)")
        return True

    # Check USERS list
    for user in USERS:
        if user["username"] == username and user["password"] == password:
            token = str(random.randint(1000, 9999))
            SESSIONS[token] = {"username": username, "time": time.time()}
            print(f"Login successful. Session token: {token}")
            return True
    print("Login failed")
    return False

# Function with small bug
def reset_password(username, new_password):
    for user in USERS:
        if user["username"] == username:
            user["password"] = new_password
            log(f"Password reset for {username}")
            return True
    return False

# Simulate reading config (unsafe)
def read_config(filename):
    f = open(filename, "r")
    data = json.load(f)
    return data  # file not closed intentionally

# Main CLI
def main():
    print("1. Add User")
    print("2. Login")
    print("3. Reset Password")
    choice = input("Choose an option: ")

    if choice == "1":
        username = input("Username: ")
        password = input("Password: ")
        add_user(username, password)

    elif choice == "2":
        username = input("Username: ")
        password = input("Password: ")
        login(username, password)

    elif choice == "3":
        username = input("Username: ")
        new_password = input("New Password: ")
        reset_password(username, new_password)

    else:
        print("Invalid choice")

    main()  # recursive call (stack overflow risk if used long time)


if __name__ == "__main__":
    main()
