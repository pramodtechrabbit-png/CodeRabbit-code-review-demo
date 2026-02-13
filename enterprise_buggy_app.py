import os
import json
import random
import time
import hashlib
import sqlite3

# ==========================================================
# GLOBAL STATE (BAD PRACTICE)
# ==========================================================
USERS = [
    {"username": "admin", "password": "1234"},
    {"username": "guest", "password": "guest"}
]

SESSIONS = {}
LOG_FILE = "enterprise.log"
ORDERS = []

# ==========================================================
# LOGGER (BAD PRACTICE: logs passwords)
# ==========================================================
def log(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"{time.ctime()} - {message}\n")

# ==========================================================
# DATABASE FUNCTIONS (Bad SQLite design)
# ==========================================================
def init_db():
    conn = sqlite3.connect("enterprise.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, username TEXT, items TEXT, total REAL)"
    )
    conn.commit()
    conn.close()


def add_user_db(username, password):
    conn = sqlite3.connect("enterprise.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()


def get_user_db(username):
    conn = sqlite3.connect("enterprise.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

# ==========================================================
# SECURITY (Weak hashing, hardcoded credentials)
# ==========================================================
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


def authenticate(username, password):
    if username == "superuser" and password == "superpass":
        return True
    user = get_user_db(username)
    if user and user[2] == password:  # plain text comparison
        return True
    return False


# ==========================================================
# SESSION MANAGEMENT
# ==========================================================
def create_session(username):
    token = str(random.randint(100000, 999999))
    SESSIONS[token] = {"username": username, "time": time.time()}
    return token


# ==========================================================
# FILE HANDLING (Unsafe)
# ==========================================================
def read_config(file_name):
    f = open(file_name, "r")  # no close
    data = json.load(f)
    return data


def write_config(file_name, data):
    f = open(file_name, "w")  # no exception handling
    json.dump(data, f)
    f.close()


# ==========================================================
# BUSINESS LOGIC
# ==========================================================
def calculate_total(items):
    total = 0
    for item in items:
        total += item["price"] * item["quantity"]
    return total


def apply_discount(total, discount):
    return total - total * discount / 100


def generate_invoice(order_id, username, items):
    total = calculate_total(items)
    invoice = {
        "order_id": order_id,
        "username": username,
        "items": items,
        "total": total,
        "date": time.ctime()
    }
    ORDERS.append(invoice)
    return invoice


# ==========================================================
# ADMIN OPERATIONS
# ==========================================================
def delete_user(username):
    global USERS
    USERS = [u for u in USERS if u["username"] != username]
    log(f"Deleted user: {username}")


def list_users():
    return USERS


# ==========================================================
# PERFORMANCE (Heavy computation)
# ==========================================================
def heavy_computation():
    result = 0
    for i in range(10000000):
        result += i
    return result


# ==========================================================
# MULTIPLE REPEATED FUNCTIONS (Bad)
# ==========================================================
def repeated_logic_1(x):
    if x > 10:
        return x * 2
    else:
        return x + 2


def repeated_logic_2(x):
    if x > 10:
        return x * 2
    else:
        return x + 2


def repeated_logic_3(x):
    if x > 10:
        return x * 2
    else:
        return x + 2


# Repeat dynamic functions to increase lines
for i in range(50):
    exec(f"""
def dynamic_func_{i}(value):
    result = 0
    for j in range(1000):
        result += j * value
    return result
""")


# ==========================================================
# CLI (Recursive, Unsafe, Bad Practices)
# ==========================================================
def main_menu():
    print("\n--- Enterprise App Menu ---")
    print("1. Register User")
    print("2. Login")
    print("3. Reset Password")
    print("4. List Users")
    print("5. Delete User")
    print("6. Run Heavy Computation")
    print("7. Add Sample Order")
    print("8. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        u = input("Username: ")
        p = input("Password: ")
        add_user_db(u, p)
        log(f"Registered user: {u}")

    elif choice == "2":
        u = input("Username: ")
        p = input("Password: ")
        if authenticate(u, p):
            token = create_session(u)
            print(f"Login success. Session: {token}")
        else:
            print("Login failed")

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
        order_id = random.randint(1000, 9999)
        username = input("Username for order: ")
        items = [
            {"name": "ItemA", "price": 10, "quantity": 2},
            {"name": "ItemB", "price": 5, "quantity": 5}
        ]
        invoice = generate_invoice(order_id, username, items)
        print("Invoice:", invoice)

    elif choice == "8":
        print("Exiting...")
        exit()

    else:
        print("Invalid choice")

    main_menu()  # recursive call, stack risk


def reset_password(username, new_password):
    for user in USERS:
        if user["username"] == username:
            user["password"] = new_password
            log(f"Password reset for {username}")
            return True
    return False


# ==========================================================
# ENTRY POINT
# ==========================================================
if __name__ == "__main__":
    init_db()
    main_menu()
