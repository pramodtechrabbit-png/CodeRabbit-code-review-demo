import pytest
import hashlib
import json
import os
import tempfile
from unittest.mock import patch, mock_open, MagicMock
import login_app


@pytest.fixture
def reset_globals():
    """Reset global state before each test."""
    # Reset to known initial state
    login_app.USERS = [
        {"username": "admin", "password": "1234"},
        {"username": "guest", "password": "guest"}
    ]
    login_app.SESSIONS = {}
    yield
    # Reset again after test
    login_app.USERS = [
        {"username": "admin", "password": "1234"},
        {"username": "guest", "password": "guest"}
    ]
    login_app.SESSIONS = {}


@pytest.fixture
def temp_log_file(tmp_path):
    """Create a temporary log file."""
    log_file = tmp_path / "login.log"
    return str(log_file)


class TestHashPassword:
    """Tests for hash_password function."""

    def test_hash_password_basic(self):
        """Test basic password hashing."""
        password = "test123"
        result = login_app.hash_password(password)
        expected = hashlib.md5(password.encode()).hexdigest()
        assert result == expected

    def test_hash_password_empty_string(self):
        """Test hashing empty string."""
        result = login_app.hash_password("")
        expected = hashlib.md5("".encode()).hexdigest()
        assert result == expected

    def test_hash_password_special_chars(self):
        """Test hashing password with special characters."""
        password = "p@$$w0rd!#%"
        result = login_app.hash_password(password)
        expected = hashlib.md5(password.encode()).hexdigest()
        assert result == expected

    def test_hash_password_consistency(self):
        """Test that same password produces same hash."""
        password = "consistent"
        hash1 = login_app.hash_password(password)
        hash2 = login_app.hash_password(password)
        assert hash1 == hash2


class TestLog:
    """Tests for log function."""

    def test_log_writes_message(self, tmp_path):
        """Test that log writes message to file."""
        log_file = tmp_path / "login.log"
        test_message = "Test log message"

        with patch("login_app.open", mock_open()) as mock_file:
            login_app.log(test_message)
            mock_file.assert_called_once_with("login.log", "a")
            handle = mock_file()
            # Check that write was called with message containing the test message
            written = "".join([call[0][0] for call in handle.write.call_args_list])
            assert test_message in written

    def test_log_appends_to_file(self):
        """Test that log appends to file."""
        with patch("login_app.open", mock_open()) as mock_file:
            login_app.log("First message")
            mock_file.assert_called_with("login.log", "a")


class TestAddUser:
    """Tests for add_user function."""

    def test_add_user_success(self, reset_globals, capsys):
        """Test successfully adding a new user."""
        initial_count = len(login_app.USERS)

        with patch("login_app.log"):
            login_app.add_user("newuser", "newpass")

        assert len(login_app.USERS) == initial_count + 1
        assert {"username": "newuser", "password": "newpass"} in login_app.USERS

        captured = capsys.readouterr()
        assert "User added!" in captured.out

    def test_add_user_calls_log(self, reset_globals):
        """Test that add_user logs the action."""
        with patch("login_app.log") as mock_log:
            login_app.add_user("testuser", "testpass")
            mock_log.assert_called_once()
            call_args = mock_log.call_args[0][0]
            assert "testuser" in call_args
            assert "testpass" in call_args

    def test_add_user_with_empty_credentials(self, reset_globals):
        """Test adding user with empty credentials."""
        with patch("login_app.log"):
            login_app.add_user("", "")

        assert {"username": "", "password": ""} in login_app.USERS

    def test_add_user_duplicate_username(self, reset_globals):
        """Test adding user with duplicate username (allowed in current implementation)."""
        with patch("login_app.log"):
            login_app.add_user("admin", "newpass")

        # Check that duplicate is added (current behavior)
        admin_users = [u for u in login_app.USERS if u["username"] == "admin"]
        assert len(admin_users) >= 2


class TestLogin:
    """Tests for login function."""

    def test_login_superadmin_success(self, reset_globals, capsys):
        """Test login with hardcoded superadmin credentials."""
        result = login_app.login("superadmin", "super123")
        assert result is True

        captured = capsys.readouterr()
        assert "Login successful (superadmin)" in captured.out

    def test_login_regular_user_success(self, reset_globals, capsys):
        """Test login with regular user credentials."""
        result = login_app.login("admin", "1234")
        assert result is True

        captured = capsys.readouterr()
        assert "Login successful" in captured.out
        assert "Session token:" in captured.out

    def test_login_creates_session_token(self, reset_globals):
        """Test that login creates a session token."""
        initial_sessions = len(login_app.SESSIONS)
        login_app.login("admin", "1234")
        assert len(login_app.SESSIONS) == initial_sessions + 1

    def test_login_invalid_username(self, reset_globals, capsys):
        """Test login with invalid username."""
        result = login_app.login("nonexistent", "password")
        assert result is False

        captured = capsys.readouterr()
        assert "Login failed" in captured.out

    def test_login_invalid_password(self, reset_globals, capsys):
        """Test login with invalid password."""
        result = login_app.login("admin", "wrongpassword")
        assert result is False

        captured = capsys.readouterr()
        assert "Login failed" in captured.out

    def test_login_empty_credentials(self, reset_globals, capsys):
        """Test login with empty credentials."""
        result = login_app.login("", "")
        assert result is False

        captured = capsys.readouterr()
        assert "Login failed" in captured.out

    def test_login_guest_user(self, reset_globals):
        """Test login with guest user."""
        result = login_app.login("guest", "guest")
        assert result is True

    def test_login_case_sensitive(self, reset_globals):
        """Test that login is case-sensitive."""
        result = login_app.login("ADMIN", "1234")
        assert result is False

    def test_login_session_contains_username(self, reset_globals):
        """Test that session contains username."""
        login_app.login("admin", "1234")
        # Find the session with admin
        admin_session = None
        for token, session in login_app.SESSIONS.items():
            if session.get("username") == "admin":
                admin_session = session
                break

        assert admin_session is not None
        assert admin_session["username"] == "admin"
        assert "time" in admin_session


class TestResetPassword:
    """Tests for reset_password function."""

    def test_reset_password_success(self, reset_globals):
        """Test successfully resetting password."""
        with patch("login_app.log"):
            result = login_app.reset_password("admin", "newpassword")

        assert result is True
        # Find admin user and check password
        admin_user = next((u for u in login_app.USERS if u["username"] == "admin"), None)
        assert admin_user is not None
        assert admin_user["password"] == "newpassword"

    def test_reset_password_nonexistent_user(self, reset_globals):
        """Test resetting password for nonexistent user."""
        with patch("login_app.log"):
            result = login_app.reset_password("nonexistent", "newpass")

        assert result is False

    def test_reset_password_calls_log(self, reset_globals):
        """Test that reset_password logs the action."""
        with patch("login_app.log") as mock_log:
            login_app.reset_password("admin", "newpass")
            mock_log.assert_called_once()
            call_args = mock_log.call_args[0][0]
            assert "admin" in call_args

    def test_reset_password_empty_password(self, reset_globals):
        """Test resetting password to empty string."""
        with patch("login_app.log"):
            result = login_app.reset_password("admin", "")

        assert result is True
        admin_user = next((u for u in login_app.USERS if u["username"] == "admin"), None)
        assert admin_user["password"] == ""

    def test_reset_password_multiple_times(self, reset_globals):
        """Test resetting password multiple times."""
        with patch("login_app.log"):
            login_app.reset_password("admin", "pass1")
            login_app.reset_password("admin", "pass2")
            login_app.reset_password("admin", "pass3")

        admin_user = next((u for u in login_app.USERS if u["username"] == "admin"), None)
        assert admin_user["password"] == "pass3"


class TestReadConfig:
    """Tests for read_config function."""

    def test_read_config_valid_json(self, tmp_path):
        """Test reading valid JSON config."""
        config_file = tmp_path / "config.json"
        test_data = {"key1": "value1", "key2": "value2"}
        config_file.write_text(json.dumps(test_data))

        result = login_app.read_config(str(config_file))
        assert result == test_data

    def test_read_config_nested_json(self, tmp_path):
        """Test reading nested JSON config."""
        config_file = tmp_path / "config.json"
        test_data = {
            "database": {
                "host": "localhost",
                "port": 5432
            },
            "settings": {
                "debug": True
            }
        }
        config_file.write_text(json.dumps(test_data))

        result = login_app.read_config(str(config_file))
        assert result == test_data
        assert result["database"]["host"] == "localhost"

    def test_read_config_empty_json(self, tmp_path):
        """Test reading empty JSON object."""
        config_file = tmp_path / "config.json"
        config_file.write_text("{}")

        result = login_app.read_config(str(config_file))
        assert result == {}

    def test_read_config_file_not_found(self):
        """Test reading nonexistent config file."""
        with pytest.raises(FileNotFoundError):
            login_app.read_config("nonexistent.json")

    def test_read_config_invalid_json(self, tmp_path):
        """Test reading invalid JSON."""
        config_file = tmp_path / "config.json"
        config_file.write_text("not valid json")

        with pytest.raises(json.JSONDecodeError):
            login_app.read_config(str(config_file))


class TestMainIntegration:
    """Integration tests for main function flow."""

    def test_main_add_user_flow(self, reset_globals):
        """Test main function with add user flow."""
        # Create infinite mock that raises StopIteration after processing one flow
        inputs = ["1", "testuser", "testpass"]
        with patch("builtins.input", side_effect=inputs + [StopIteration()]) as mock_input, \
             patch("login_app.log"), \
             pytest.raises(StopIteration):
            login_app.main()

    def test_main_login_flow(self, reset_globals):
        """Test main function with login flow."""
        inputs = ["2", "admin", "1234"]
        with patch("builtins.input", side_effect=inputs + [StopIteration()]) as mock_input, \
             pytest.raises(StopIteration):
            login_app.main()

    def test_main_reset_password_flow(self, reset_globals):
        """Test main function with reset password flow."""
        inputs = ["3", "admin", "newpass"]
        with patch("builtins.input", side_effect=inputs + [StopIteration()]) as mock_input, \
             patch("login_app.log"), \
             pytest.raises(StopIteration):
            login_app.main()

    def test_main_invalid_choice(self, reset_globals, capsys):
        """Test main function with invalid choice."""
        with patch("builtins.input", side_effect=["99", StopIteration()]) as mock_input, \
             pytest.raises(StopIteration):
            login_app.main()


class TestEdgeCases:
    """Additional edge case tests."""

    def test_session_token_uniqueness(self, reset_globals):
        """Test that session tokens are reasonably unique."""
        # Test that we can create multiple sessions
        tokens = []
        for _ in range(10):
            result = login_app.login("admin", "1234")
            if result:
                # Get the most recent token
                if login_app.SESSIONS:
                    tokens.append(list(login_app.SESSIONS.keys())[-1])

        # Should have created multiple sessions
        assert len(tokens) >= 10
        # Most tokens should be unique (some might collide due to random)
        assert len(set(tokens)) >= 5

    def test_login_after_password_reset(self, reset_globals):
        """Test login works after password reset."""
        with patch("login_app.log"):
            login_app.reset_password("admin", "newpass123")

        # Old password should fail
        result1 = login_app.login("admin", "1234")
        assert result1 is False

        # New password should work
        result2 = login_app.login("admin", "newpass123")
        assert result2 is True

    def test_add_user_then_login(self, reset_globals):
        """Test adding user and then logging in."""
        with patch("login_app.log"):
            login_app.add_user("newuser", "newpass")

        result = login_app.login("newuser", "newpass")
        assert result is True

    def test_users_list_persistence_across_operations(self, reset_globals):
        """Test that USERS list persists across operations."""
        initial_count = len(login_app.USERS)

        with patch("login_app.log"):
            login_app.add_user("user1", "pass1")
            login_app.add_user("user2", "pass2")

        assert len(login_app.USERS) == initial_count + 2

        # Login should still work with new users
        assert login_app.login("user1", "pass1") is True
        assert login_app.login("user2", "pass2") is True