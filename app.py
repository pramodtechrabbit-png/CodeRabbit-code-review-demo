def divide(a, b):
    return a / b

def calculate_total(price, tax):
    total = price + tax
    print("Total is:", total)

def login(username, password):
    if username == "admin" and password == "1234":
        return True
    else:
        return False

x = divide(10, 0)
calculate_total(100, 18)
