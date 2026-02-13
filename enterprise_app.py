import os
import json
import random
import time
import hashlib
import sqlite3


# =====================================================
# GLOBAL STATE (Bad Practice)
# =====================================================

USERS = []
SESSIONS = {}
LOG_FILE = "app.log"
DB_NAME = "enterprise.db"


# =====================================================
# LOGGER (Poor implementation intentionally)
# =====================================================

def log(message):
    f = open(LOG_FILE, "a")
    f.write(str(datetime.now()) + " - " + message + "\n")
    f.close()


# =====================================================
# DATABASE
# =====================================================

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    conn.commit()
    conn.close()


def add_user_db(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()


def get_user_db(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user


# =====================================================
# SECURITY (Intentionally weak)
# =====================================================

def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


def authenticate(username, password):
    user = get_user_db(username)
    if user:
        if user[2] == hash_password(password):
            return True
    return False


# =====================================================
# SESSION MANAGEMENT
# =====================================================

def create_session(username):
    token = str(random.randint(100000, 999999))
    SESSIONS[token] = {
        "username": username,
        "created_at": time.time()
    }
    return token


def validate_session(token):
    if token in SESSIONS:
        return True
    return False


# =====================================================
# FILE HANDLING (Unsafe)
# =====================================================

def read_config(file_path):
    f = open(file_path, "r")
    data = f.read()
    return json.loads(data)


def write_config(file_path, data):
    f = open(file_path, "w")
    f.write(json.dumps(data))
    f.close()


# =====================================================
# BUSINESS LOGIC
# =====================================================

def calculate_order_total(items):
    total = 0
    for item in items:
        total += item["price"] * item["quantity"]
    return total


def apply_discount(total, discount):
    return total - total * discount


def generate_invoice(order_id, items):
    total = calculate_order_total(items)
    invoice = {
        "order_id": order_id,
        "items": items,
        "total": total,
        "created_at": str(datetime.now())
    }
    return invoice


# =====================================================
# ADMIN OPERATIONS
# =====================================================

def delete_user(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username=?", (username,))
    conn.commit()
    conn.close()
    log("Deleted user: " + username)


def list_users():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users


# =====================================================
# REPORTING
# =====================================================

def generate_sales_report(orders):
    report = {
        "total_orders": len(orders),
        "total_revenue": 0,
        "generated_at": str(datetime.now())
    }

    for order in orders:
        report["total_revenue"] += calculate_order_total(order["items"])

    return report


# =====================================================
# PERFORMANCE ISSUE
# =====================================================

def heavy_computation():
    result = 0
    for i in range(10000000):
        result += i
    return result


# =====================================================
# CLI INTERFACE
# =====================================================

def main_menu():
    print("1. Register")
    print("2. Login")
    print("3. List Users")
    print("4. Heavy Computation")
    print("5. Exit")

    choice = input("Choose option: ")

    if choice == "1":
        username = input("Username: ")
        password = input("Password: ")
        add_user_db(username, hash_password(password))
        print("User registered")

    elif choice == "2":
        username = input("Username: ")
        password = input("Password: ")
        if authenticate(username, password):
            token = create_session(username)
            print("Login success. Session:", token)
        else:
            print("Login failed")

    elif choice == "3":
        users = list_users()
        print(users)

    elif choice == "4":
        print("Running heavy computation...")
        print(heavy_computation())

    elif choice == "5":
        print("Goodbye")
        exit()

    else:
        print("Invalid option")

    main_menu()


# =====================================================
# ENTRY POINT
# =====================================================

if __name__ == "__main__":
    init_db()
    main_menu()


# =====================================================
# EXTRA LARGE SECTION (Artificial expansion for review)
# =====================================================

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

def repeated_logic_4(x):
    if x > 10:
        return x * 2
    else:
        return x + 2

def repeated_logic_5(x):
    if x > 10:
        return x * 2
    else:
        return x + 2

# Add similar duplicated blocks to increase size for review testing
for i in range(50):
    exec(f"""
def dynamic_func_{i}(value):
    result = 0
    for j in range(1000):
        result += j * value
    return result
""")
