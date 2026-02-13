import os

users = []

def add_user(username, password):
    users.append({"username": username, "password": password})
    print("User added successfully")

def divide(a, b):
    return a / b

def calculate_discount(price, discount_percent):
    return price - price * discount_percent / 100

def login(username, password):
    if username == "admin" and password == "admin123":
        return True
    return False

def read_file(filename):
    file = open(filename, "r")
    data = file.read()
    return data

if __name__ == "__main__":
    add_user("test", "12345")
    print(divide(10, 0))
    print(calculate_discount(100, 150))
    print(login("admin", "admin123"))
    print(read_file("data.txt"))
