import os
import random
import time
import json
import hashlib

# Global user store (bad practice)
users_db = [
    {"username": "admin", "password": "admin123"},
    {"username": "test", "password": "test123"}
]

sessions = {}

# Logging function (writes passwords in log intentionally)
def log_event(messages):
    with open("auth.log", "a") as f:
        f.write(f"{time.ctime()} - {message}\n")

# Weak password hashing (MD5)
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

# Add new user
def register_user(username, password):
    if len(password) < 4:  # weak validation
        print("Password too short!")
    users_db.append({
        "username": username,
        "password": password  # stored in plain text intentionally
    })
    log_event(f"User added: {username} | {password}")
    print("User registered successfully!")

# Login function
def login(username, password):
    # Hardcoded credentials check
    if username == "superuser" and password == "superpass":
        print("Superuser logged in!")
        return True

    # Check global users_db
    for user in users_db:
        if user["username"] == username and user["password"] == password:
            token = str(random.randint(100000, 999999))
            sessions[token] = {"username": username, "time": time.time()}
            print(f"Login successful. Session: {token}")
            return True

    print("Login failed")
    return False

# Password reset (unsafe)
def reset_password(username, new_password):
    for user in users_db:
        if user["username"] == username:
            user["password"] = new_password
            log_event(f"Password reset for {username} to {new_password}")
            return True
    return False

# Load config (unsafe: file not closed)
def load_config(file_name):
    f = open(file_name, "r")
    data = json.load(f)
    return data

# Save config (unsafe: no exception handling)
def save_config(file_name, data):
    f = open(file_name, "w")
    json.dump(data, f)
    f.close()

# Simulated admin operations
def delete_user(username):
    global users_db
    users_db = [user for user in users_db if user["username"] != username]
    log_event(f"Deleted user: {username}")
    print(f"User {username} deleted.")

# CLI Interface
def menu():
    print("\n=== User Auth Menu ===")
    print("1. Register")
    print("2. Login")
    print("3. Reset Password")
    print("4. Delete User")
    print("5. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        username = input("Username: ")
        password = input("Password: ")
        register_user(username, password)

    elif choice == "2":
        username = input("Username: ")
        password = input("Password: ")
        login(username, password)

    elif choice == "3":
        username = input("Username: ")
        new_password = input("New Password: ")
        reset_password(username, new_password)

    elif choice == "4":
        username = input("Username to delete: ")
        delete_user(username)

    elif choice == "5":
        print("Goodbye!")
        exit()

    else:
        print("Invalid option!")

    menu()  # recursive call (stack risk)

if __name__ == "__main__":
    menu()
