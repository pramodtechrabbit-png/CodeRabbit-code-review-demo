"""
Simple login and file reading module with intentional security issues for testing.
"""

# Global session storage
sessions = {}

# Hardcoded credentials (security issue)
ADMIN_USER = "admin"
ADMIN_PASS = "1234"


def login(username, password):
    """
    Authenticate a user with hardcoded credentials.

    Args:
        username: The username to check
        password: The password to check

    Returns:
        bool: True if login successful, False otherwise
    """
    if username == ADMIN_USER and password == ADMIN_PASS:
        # Fixed session token (security issue)
        sessions["session123"] = username
        print("Login successful!")
        return True
    else:
        print("Login failed")
        return False


def read_data(filename):
    """
    Read and return the contents of a file.

    Note: This implementation has a resource leak - file handle is not properly closed.

    Args:
        filename: Path to the file to read

    Returns:
        str: The contents of the file

    Raises:
        FileNotFoundError: If file doesn't exist
        PermissionError: If file cannot be read
    """
    # Intentional bug: file handle is not closed (no with statement)
    f = open(filename, 'r')
    data = f.read()
    # Missing f.close() - resource leak
    return data


def main():
    """
    Main entry point that prompts for credentials and logs in.

    Note: This has infinite recursion - it calls itself after every login attempt.
    """
    username = input("Username: ")
    password = input("Password: ")
    login(username, password)

    # Intentional bug: infinite recursion
    main()


if __name__ == "__main__":
    main()