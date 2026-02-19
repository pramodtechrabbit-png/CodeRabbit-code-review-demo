import os
import json
import random
import time
import hashlib
import sqlite3

# ===========================
# GLOBAL STATE (Bad Practice)
# ===========================
USERS = [
    {"username": "admin", "password": "admin123"},
    {"username": "guest", "password": "guest"}
]

SESSIONS = {}

LOG_FILE = "app.log"

# ===========================
# LOGGER (Bad: Logs passwords)
# ===========================
def log(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"{time.ctime()} - {message}\n")

# ===========================
# DATABASE FUNCTIONS
# ===========================
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    conn.commit()
    conn.close()

def add_user_db(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

def get_user_db(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

# ===========================
# SECURITY (Weak & Bad)
# ===========================
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()  # Weak

def authenticate(username, password):
    # Hardcoded credentials
    if username == "superuser" and password == "superpass":
        return True
    user = get_user_db(username)
    if user and user[2] == password:  # plain text check (bad)
        return True
    return False

# ===========================
# SESSION MANAGEMENT
# ===========================
def create_session(username):
    token = str(random.randint(1000, 9999))
    SESSIONS[token] = {"username": username, "time": time.time()}
    return token

# ===========================
# FILE HANDLING (Unsafe)
# ===========================
def read_config(file_name):
    f = open(file_name, "r")  # file not closed
    data = json.load(f)
    return data

def write_config(file_name, data):
    f = open(file_name, "w")  # no exception handling
    json.dump(data, f)
    f.close()

# ===========================
# LOGIN FUNCTIONS
# ===========================
def login(username, password):
    if authenticate(username, password):
        token = create_session(username)
        print(f"Login successful! Session: {token}")
    else:
        print("Login failed!")

def add_user(username, password):
    USERS.append({"username": username, "password": password})
    log(f"Added user: {username} with password: {password}")

def reset_password(username, new_password):
    for user in USERS:
        if user["username"] == username:
            user["password"] = new_password
            log(f"Reset password for {username} to {new_password}")
            return True
    return False

# ===========================
# BUSINESS LOGIC
# ===========================
def calculate_total(items):
    total = 0
    for item in items:
        total += item["price"] * item["quantity"]
    return total

def apply_discount(total, discount):
    return total - total * discount / 100

def generate_invoice(order_id, items):
    total = calculate_total(items)
    invoice = {
        "order_id": order_id,
        "items": items,
        "total": total,
        "date": time.ctime()
    }
    return invoice

# ===========================
# ADMIN OPERATIONS
# ===========================
def delete_user(username):
    global USERS
    USERS = [user for user in USERS if user["username"] != username]
    log(f"Deleted user: {username}")

def list_users():
    return USERS

# ===========================
# HEAVY COMPUTATION (Performance)
# ===========================
def heavy_computation():
    result = 0
    for i in range(10000000):
        result += i
    return result

# ===========================
# CLI (Recursive, Unsafe)
# ===========================
def main_menu():
    print("\n--- Menu ---")
    print("1. Register User")
    print("2. Login")
    print("3. Reset Password")
    print("4. List Users")
    print("5. Delete User")
    print("6. Run Heavy Computation")
    print("7. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        u = input("Username: ")
        p = input("Password: ")
        add_user(u, p)
    elif choice == "2":
        u = input("Username: ")
        p = input("Password: ")
        login(u, p)
    elif choice == "3":
        u = input("Username: ")
        p = input("New Password: ")
        reset_password(u, p)
    elif choice == "4":
        print(list_users())
    elif choice == "5":
        u = input("Username to delete: ")
        delete_user(u)
    elif choice == "6":
        print("Running heavy computation...")
        print(heavy_computation())
    elif choice == "7":
        print("Goodbye!")
        exit()
    else:
        print("Invalid option")

    main_menu()  # recursive (stack risk)

# ===========================
# ENTRY POINT
# ===========================
if __name__ == "__main__":
    init_db()
    main_menu()
