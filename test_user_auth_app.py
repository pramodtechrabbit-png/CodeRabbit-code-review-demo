import pytest
import hashlib
import json
import os
import tempfile
from unittest.mock import patch, mock_open, MagicMock
import user_auth_app


@pytest.fixture
def reset_globals():
    """Reset global state before each test."""
    # Reset to known initial state
    user_auth_app.users_db = [
        {"username": "admin", "password": "admin123"},
        {"username": "test", "password": "test123"}
    ]
    user_auth_app.sessions = {}
    yield
    # Reset again after test
    user_auth_app.users_db = [
        {"username": "admin", "password": "admin123"},
        {"username": "test", "password": "test123"}
    ]
    user_auth_app.sessions = {}


@pytest.fixture
def temp_log_file(tmp_path):
    """Create a temporary log file."""
    log_file = tmp_path / "auth.log"
    return str(log_file)


class TestHashPassword:
    """Tests for hash_password function."""

    def test_hash_password_basic(self):
        """Test basic password hashing."""
        password = "test123"
        result = user_auth_app.hash_password(password)
        expected = hashlib.md5(password.encode()).hexdigest()
        assert result == expected

    def test_hash_password_empty_string(self):
        """Test hashing empty string."""
        result = user_auth_app.hash_password("")
        expected = hashlib.md5("".encode()).hexdigest()
        assert result == expected

    def test_hash_password_special_chars(self):
        """Test hashing password with special characters."""
        password = "p@$$w0rd!#%^&*()"
        result = user_auth_app.hash_password(password)
        expected = hashlib.md5(password.encode()).hexdigest()
        assert result == expected

    def test_hash_password_unicode(self):
        """Test hashing password with unicode characters."""
        password = "пароль123"  # Russian characters
        result = user_auth_app.hash_password(password)
        expected = hashlib.md5(password.encode()).hexdigest()
        assert result == expected

    def test_hash_password_consistency(self):
        """Test that same password produces same hash."""
        password = "consistent"
        hash1 = user_auth_app.hash_password(password)
        hash2 = user_auth_app.hash_password(password)
        assert hash1 == hash2


class TestLogEvent:
    """Tests for log_event function."""

    def test_log_event_writes_message(self):
        """Test that log_event writes message to file."""
        with patch("user_auth_app.open", mock_open()) as mock_file:
            user_auth_app.log_event("Test message")
            mock_file.assert_called_once_with("auth.log", "a")
            handle = mock_file()
            written = "".join([call[0][0] for call in handle.write.call_args_list])
            assert "Test message" in written

    def test_log_event_function_signature(self):
        """Test that log_event has correct parameter name."""
        import inspect
        sig = inspect.signature(user_auth_app.log_event)
        params = list(sig.parameters.keys())
        assert "message" in params  # Parameter is named 'message'


class TestRegisterUser:
    """Tests for register_user function."""

    def test_register_user_success(self, reset_globals, capsys):
        """Test successfully registering a new user."""
        initial_count = len(user_auth_app.users_db)

        with patch("user_auth_app.log_event"):
            user_auth_app.register_user("newuser", "newpass123")

        assert len(user_auth_app.users_db) == initial_count + 1
        assert {"username": "newuser", "password": "newpass123"} in user_auth_app.users_db

        captured = capsys.readouterr()
        assert "User registered successfully!" in captured.out

    def test_register_user_short_password_warning(self, reset_globals, capsys):
        """Test registering user with short password shows warning."""
        with patch("user_auth_app.log_event"):
            user_auth_app.register_user("user", "abc")

        captured = capsys.readouterr()
        assert "Password too short!" in captured.out

    def test_register_user_short_password_still_added(self, reset_globals):
        """Test that user is still added even with short password."""
        initial_count = len(user_auth_app.users_db)

        with patch("user_auth_app.log_event"):
            user_auth_app.register_user("user", "abc")

        # User is still added despite warning
        assert len(user_auth_app.users_db) == initial_count + 1

    def test_register_user_minimum_valid_password(self, reset_globals):
        """Test registering user with minimum valid password length."""
        with patch("user_auth_app.log_event"):
            user_auth_app.register_user("user", "1234")

        assert {"username": "user", "password": "1234"} in user_auth_app.users_db

    def test_register_user_empty_username(self, reset_globals):
        """Test registering user with empty username."""
        with patch("user_auth_app.log_event"):
            user_auth_app.register_user("", "password123")

        assert {"username": "", "password": "password123"} in user_auth_app.users_db

    def test_register_user_duplicate_username(self, reset_globals):
        """Test registering duplicate username (allowed in current implementation)."""
        with patch("user_auth_app.log_event"):
            user_auth_app.register_user("admin", "newpass")

        # Check that duplicate is added
        admin_users = [u for u in user_auth_app.users_db if u["username"] == "admin"]
        assert len(admin_users) >= 2

    def test_register_user_calls_log_event(self, reset_globals):
        """Test that register_user attempts to call log_event."""
        with patch("user_auth_app.log_event") as mock_log:
            user_auth_app.register_user("testuser", "testpass")
            mock_log.assert_called_once()


class TestLogin:
    """Tests for login function."""

    def test_login_superuser_success(self, reset_globals, capsys):
        """Test login with hardcoded superuser credentials."""
        result = user_auth_app.login("superuser", "superpass")
        assert result is True

        captured = capsys.readouterr()
        assert "Superuser logged in!" in captured.out

    def test_login_regular_user_success(self, reset_globals, capsys):
        """Test login with regular user credentials."""
        result = user_auth_app.login("admin", "admin123")
        assert result is True

        captured = capsys.readouterr()
        assert "Login successful" in captured.out
        assert "Session:" in captured.out

    def test_login_creates_session_token(self, reset_globals):
        """Test that login creates a session token."""
        initial_sessions = len(user_auth_app.sessions)
        user_auth_app.login("admin", "admin123")
        assert len(user_auth_app.sessions) == initial_sessions + 1

    def test_login_session_token_length(self, reset_globals):
        """Test that session token is 6 digits."""
        user_auth_app.login("admin", "admin123")
        # Get the last added session token
        token = list(user_auth_app.sessions.keys())[-1]
        assert len(token) == 6
        assert token.isdigit()

    def test_login_invalid_username(self, reset_globals, capsys):
        """Test login with invalid username."""
        result = user_auth_app.login("nonexistent", "password")
        assert result is False

        captured = capsys.readouterr()
        assert "Login failed" in captured.out

    def test_login_invalid_password(self, reset_globals, capsys):
        """Test login with invalid password."""
        result = user_auth_app.login("admin", "wrongpassword")
        assert result is False

        captured = capsys.readouterr()
        assert "Login failed" in captured.out

    def test_login_empty_credentials(self, reset_globals, capsys):
        """Test login with empty credentials."""
        result = user_auth_app.login("", "")
        assert result is False

        captured = capsys.readouterr()
        assert "Login failed" in captured.out

    def test_login_test_user(self, reset_globals):
        """Test login with test user."""
        result = user_auth_app.login("test", "test123")
        assert result is True

    def test_login_case_sensitive(self, reset_globals):
        """Test that login is case-sensitive."""
        result = user_auth_app.login("ADMIN", "admin123")
        assert result is False

    def test_login_session_contains_correct_data(self, reset_globals):
        """Test that session contains username and time."""
        user_auth_app.login("admin", "admin123")
        # Find the session with admin
        admin_session = None
        for token, session in user_auth_app.sessions.items():
            if session.get("username") == "admin":
                admin_session = session
                break

        assert admin_session is not None
        assert admin_session["username"] == "admin"
        assert "time" in admin_session

    def test_login_multiple_sessions(self, reset_globals):
        """Test creating multiple sessions."""
        user_auth_app.login("admin", "admin123")
        user_auth_app.login("test", "test123")
        assert len(user_auth_app.sessions) >= 2


class TestResetPassword:
    """Tests for reset_password function."""

    def test_reset_password_success(self, reset_globals):
        """Test successfully resetting password."""
        with patch("user_auth_app.log_event"):
            result = user_auth_app.reset_password("admin", "newpassword")

        assert result is True
        # Find admin user and check password
        admin_user = next((u for u in user_auth_app.users_db if u["username"] == "admin"), None)
        assert admin_user is not None
        assert admin_user["password"] == "newpassword"

    def test_reset_password_nonexistent_user(self, reset_globals):
        """Test resetting password for nonexistent user."""
        with patch("user_auth_app.log_event"):
            result = user_auth_app.reset_password("nonexistent", "newpass")

        assert result is False

    def test_reset_password_calls_log_event(self, reset_globals):
        """Test that reset_password attempts to call log_event."""
        with patch("user_auth_app.log_event") as mock_log:
            user_auth_app.reset_password("admin", "newpass")
            mock_log.assert_called_once()

    def test_reset_password_empty_password(self, reset_globals):
        """Test resetting password to empty string."""
        with patch("user_auth_app.log_event"):
            result = user_auth_app.reset_password("admin", "")

        assert result is True
        admin_user = next((u for u in user_auth_app.users_db if u["username"] == "admin"), None)
        assert admin_user["password"] == ""

    def test_reset_password_multiple_times(self, reset_globals):
        """Test resetting password multiple times."""
        with patch("user_auth_app.log_event"):
            user_auth_app.reset_password("admin", "pass1")
            user_auth_app.reset_password("admin", "pass2")
            user_auth_app.reset_password("admin", "pass3")

        admin_user = next((u for u in user_auth_app.users_db if u["username"] == "admin"), None)
        assert admin_user["password"] == "pass3"


class TestLoadConfig:
    """Tests for load_config function."""

    def test_load_config_valid_json(self, tmp_path):
        """Test loading valid JSON config."""
        config_file = tmp_path / "config.json"
        test_data = {"key1": "value1", "key2": "value2"}
        config_file.write_text(json.dumps(test_data))

        result = user_auth_app.load_config(str(config_file))
        assert result == test_data

    def test_load_config_nested_json(self, tmp_path):
        """Test loading nested JSON config."""
        config_file = tmp_path / "config.json"
        test_data = {
            "database": {
                "host": "localhost",
                "port": 5432,
                "credentials": {
                    "username": "dbuser",
                    "password": "dbpass"
                }
            }
        }
        config_file.write_text(json.dumps(test_data))

        result = user_auth_app.load_config(str(config_file))
        assert result == test_data
        assert result["database"]["credentials"]["username"] == "dbuser"

    def test_load_config_empty_json(self, tmp_path):
        """Test loading empty JSON object."""
        config_file = tmp_path / "config.json"
        config_file.write_text("{}")

        result = user_auth_app.load_config(str(config_file))
        assert result == {}

    def test_load_config_array(self, tmp_path):
        """Test loading JSON array."""
        config_file = tmp_path / "config.json"
        test_data = [1, 2, 3, 4, 5]
        config_file.write_text(json.dumps(test_data))

        result = user_auth_app.load_config(str(config_file))
        assert result == test_data

    def test_load_config_file_not_found(self):
        """Test loading nonexistent config file."""
        with pytest.raises(FileNotFoundError):
            user_auth_app.load_config("nonexistent.json")

    def test_load_config_invalid_json(self, tmp_path):
        """Test loading invalid JSON."""
        config_file = tmp_path / "config.json"
        config_file.write_text("not valid json {]")

        with pytest.raises(json.JSONDecodeError):
            user_auth_app.load_config(str(config_file))


class TestSaveConfig:
    """Tests for save_config function."""

    def test_save_config_basic(self, tmp_path):
        """Test saving basic config."""
        config_file = tmp_path / "config.json"
        test_data = {"key1": "value1", "key2": "value2"}

        user_auth_app.save_config(str(config_file), test_data)

        # Verify file was created and contains correct data
        assert config_file.exists()
        saved_data = json.loads(config_file.read_text())
        assert saved_data == test_data

    def test_save_config_nested(self, tmp_path):
        """Test saving nested config."""
        config_file = tmp_path / "config.json"
        test_data = {
            "settings": {
                "debug": True,
                "logging": {
                    "level": "INFO"
                }
            }
        }

        user_auth_app.save_config(str(config_file), test_data)

        saved_data = json.loads(config_file.read_text())
        assert saved_data == test_data

    def test_save_config_array(self, tmp_path):
        """Test saving array config."""
        config_file = tmp_path / "config.json"
        test_data = [1, 2, 3, 4, 5]

        user_auth_app.save_config(str(config_file), test_data)

        saved_data = json.loads(config_file.read_text())
        assert saved_data == test_data

    def test_save_config_overwrites_existing(self, tmp_path):
        """Test that save_config overwrites existing file."""
        config_file = tmp_path / "config.json"
        config_file.write_text("old content")

        test_data = {"new": "data"}
        user_auth_app.save_config(str(config_file), test_data)

        saved_data = json.loads(config_file.read_text())
        assert saved_data == test_data

    def test_save_config_empty_dict(self, tmp_path):
        """Test saving empty dictionary."""
        config_file = tmp_path / "config.json"
        user_auth_app.save_config(str(config_file), {})

        saved_data = json.loads(config_file.read_text())
        assert saved_data == {}


class TestDeleteUser:
    """Tests for delete_user function."""

    def test_delete_user_success(self, reset_globals, capsys):
        """Test successfully deleting a user."""
        initial_count = len(user_auth_app.users_db)

        with patch("user_auth_app.log_event"):
            user_auth_app.delete_user("admin")

        assert len(user_auth_app.users_db) == initial_count - 1
        assert not any(u["username"] == "admin" for u in user_auth_app.users_db)

        captured = capsys.readouterr()
        assert "User admin deleted" in captured.out

    def test_delete_user_nonexistent(self, reset_globals):
        """Test deleting nonexistent user."""
        initial_count = len(user_auth_app.users_db)

        with patch("user_auth_app.log_event"):
            user_auth_app.delete_user("nonexistent")

        # Count remains same
        assert len(user_auth_app.users_db) == initial_count

    def test_delete_user_calls_log_event(self, reset_globals):
        """Test that delete_user attempts to call log_event."""
        with patch("user_auth_app.log_event") as mock_log:
            user_auth_app.delete_user("admin")
            mock_log.assert_called_once()

    def test_delete_user_all_users(self, reset_globals):
        """Test deleting all users one by one."""
        with patch("user_auth_app.log_event"):
            user_auth_app.delete_user("admin")
            user_auth_app.delete_user("test")

        assert len(user_auth_app.users_db) == 0

    def test_delete_user_empty_username(self, reset_globals):
        """Test deleting user with empty username."""
        with patch("user_auth_app.log_event"):
            user_auth_app.delete_user("")

        # Should not affect existing users
        assert any(u["username"] == "admin" for u in user_auth_app.users_db)


class TestMenuIntegration:
    """Integration tests for menu function."""

    def test_menu_register_flow(self, reset_globals):
        """Test menu with register flow."""
        inputs = ["1", "newuser", "password123"]
        with patch("builtins.input", side_effect=inputs + [StopIteration()]), \
             patch("user_auth_app.log_event"), \
             pytest.raises(StopIteration):
            user_auth_app.menu()

    def test_menu_login_flow(self, reset_globals):
        """Test menu with login flow."""
        inputs = ["2", "admin", "admin123"]
        with patch("builtins.input", side_effect=inputs + [StopIteration()]), \
             pytest.raises(StopIteration):
            user_auth_app.menu()

    def test_menu_reset_password_flow(self, reset_globals):
        """Test menu with reset password flow."""
        inputs = ["3", "admin", "newpass"]
        with patch("builtins.input", side_effect=inputs + [StopIteration()]), \
             patch("user_auth_app.log_event"), \
             pytest.raises(StopIteration):
            user_auth_app.menu()

    def test_menu_delete_user_flow(self, reset_globals):
        """Test menu with delete user flow."""
        inputs = ["4", "test"]
        with patch("builtins.input", side_effect=inputs + [StopIteration()]), \
             patch("user_auth_app.log_event"), \
             pytest.raises(StopIteration):
            user_auth_app.menu()

    def test_menu_exit_flow(self, reset_globals):
        """Test menu with exit flow."""
        with patch("builtins.input", return_value="5"), \
             pytest.raises(SystemExit):
            user_auth_app.menu()

    def test_menu_invalid_choice(self, reset_globals, capsys):
        """Test menu with invalid choice."""
        with patch("builtins.input", side_effect=["99", StopIteration()]), \
             pytest.raises(StopIteration):
            user_auth_app.menu()


class TestEdgeCases:
    """Additional edge case tests."""

    def test_session_token_range(self, reset_globals):
        """Test that session tokens are in expected range."""
        user_auth_app.login("admin", "admin123")
        token = list(user_auth_app.sessions.keys())[-1]
        token_int = int(token)
        assert 100000 <= token_int <= 999999

    def test_login_after_password_reset(self, reset_globals):
        """Test login works after password reset."""
        with patch("user_auth_app.log_event"):
            user_auth_app.reset_password("admin", "newpass123")

        # Old password should fail
        result1 = user_auth_app.login("admin", "admin123")
        assert result1 is False

        # New password should work
        result2 = user_auth_app.login("admin", "newpass123")
        assert result2 is True

    def test_login_after_user_deleted(self, reset_globals):
        """Test login fails after user is deleted."""
        with patch("user_auth_app.log_event"):
            user_auth_app.delete_user("admin")

        result = user_auth_app.login("admin", "admin123")
        assert result is False

    def test_register_then_login(self, reset_globals):
        """Test registering user and then logging in."""
        with patch("user_auth_app.log_event"):
            user_auth_app.register_user("newuser", "newpass123")

        result = user_auth_app.login("newuser", "newpass123")
        assert result is True

    def test_multiple_operations_sequence(self, reset_globals):
        """Test sequence of multiple operations."""
        with patch("user_auth_app.log_event"):
            # Register new user
            user_auth_app.register_user("user1", "pass1")
            # Login with new user
            assert user_auth_app.login("user1", "pass1") is True
            # Reset password
            user_auth_app.reset_password("user1", "newpass1")
            # Old password fails
            assert user_auth_app.login("user1", "pass1") is False
            # New password works
            assert user_auth_app.login("user1", "newpass1") is True
            # Delete user
            user_auth_app.delete_user("user1")
            # Login fails after deletion
            assert user_auth_app.login("user1", "newpass1") is False

    def test_users_db_persistence(self, reset_globals):
        """Test that users_db persists across operations."""
        initial_count = len(user_auth_app.users_db)

        with patch("user_auth_app.log_event"):
            user_auth_app.register_user("user1", "pass1")
            user_auth_app.register_user("user2", "pass2")
            user_auth_app.delete_user("test")

        # Added 2, deleted 1
        assert len(user_auth_app.users_db) == initial_count + 1

    def test_config_save_and_load_roundtrip(self, tmp_path):
        """Test saving and loading config maintains data integrity."""
        config_file = tmp_path / "test_config.json"
        original_data = {
            "users": ["alice", "bob"],
            "settings": {"theme": "dark", "timeout": 300}
        }

        user_auth_app.save_config(str(config_file), original_data)
        loaded_data = user_auth_app.load_config(str(config_file))

        assert loaded_data == original_data

    def test_password_validation_boundary(self, reset_globals, capsys):
        """Test password validation at boundary (4 characters)."""
        with patch("user_auth_app.log_event"):
            # 3 chars - should warn
            user_auth_app.register_user("user1", "abc")
            captured = capsys.readouterr()
            assert "Password too short!" in captured.out

            # 4 chars - should not warn
            user_auth_app.register_user("user2", "abcd")
            captured = capsys.readouterr()
            assert "Password too short!" not in captured.out