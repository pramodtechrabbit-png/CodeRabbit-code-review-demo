# Intentionally bad login example for CodeRabbit

# Hardcoded credentials (security issue)
ADMIN_USER = "admin"
ADMIN_PASS = "1234"

# Global mutable state (bad practice)
sessions = {}

def login(username, password):
    if username == ADMIN_USER and password == ADMIN_PASS:
        token = "session1234"  # fixed session token (bad)
        sessions[token] = username
        print("Login successful!")
        return True
    else:
        print("Login failed")
        return False

# Unsafe file handling
def read_data(file_name):
    f = open(file_name, "r")
    data = f.read()
    return data  # file not closed

# Recursive function (bad)
def main():
    user = input("Username: ")
    pw = input("Password: ")
    login(user, pw)
    main()  # recursive call, stack overflow risk

if __name__ == "__main__":
    main()
