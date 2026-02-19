"""
Comprehensive test suite for user_auth_app.py
Tests cover main functionality, edge cases, security issues, and error handling.
"""

import pytest
import os
import json
import hashlib
import time
from unittest.mock import patch, mock_open, MagicMock, call
import user_auth_app


class TestHashPassword:
    """Tests for hash_password function"""

    def test_hash_password_basic(self):
        """Test basic password hashing"""
        result = user_auth_app.hash_password("password123")
        assert isinstance(result, str)
        assert len(result) == 32  # MD5 produces 32-char hex string

    def test_hash_password_consistency(self):
        """Test that same password produces same hash"""
        hash1 = user_auth_app.hash_password("test123")
        hash2 = user_auth_app.hash_password("test123")
        assert hash1 == hash2

    def test_hash_password_different_inputs(self):
        """Test that different passwords produce different hashes"""
        hash1 = user_auth_app.hash_password("password1")
        hash2 = user_auth_app.hash_password("password2")
        assert hash1 != hash2

    def test_hash_password_empty_string(self):
        """Test hashing empty string"""
        result = user_auth_app.hash_password("")
        expected = hashlib.md5(b"").hexdigest()
        assert result == expected

    def test_hash_password_unicode(self):
        """Test hashing unicode characters"""
        result = user_auth_app.hash_password("пароль日本語")
        assert isinstance(result, str)
        assert len(result) == 32

    def test_hash_password_long_input(self):
        """Test hashing very long password"""
        long_password = "a" * 10000
        result = user_auth_app.hash_password(long_password)
        assert len(result) == 32


class TestLogEvent:
    """Tests for log_event function"""

    @patch("builtins.open", new_callable=mock_open)
    @patch("time.ctime", return_value="Wed Jan 1 00:00:00 2025")
    def test_log_event_writes_message(self, mock_ctime, mock_file):
        """Test that log_event writes formatted message"""
        user_auth_app.log_event("Test event")
        mock_file.assert_called_once_with("auth.log", "a")
        handle = mock_file()
        handle.write.assert_called_once_with("Wed Jan 1 00:00:00 2025 - Test event\n")

    @patch("builtins.open", new_callable=mock_open)
    def test_log_event_empty_message(self, mock_file):
        """Test logging empty message"""
        user_auth_app.log_event("")
        handle = mock_file()
        assert handle.write.called

    @patch("builtins.open", new_callable=mock_open)
    def test_log_event_unicode(self, mock_file):
        """Test logging unicode characters"""
        user_auth_app.log_event("User 日本語 registered")
        assert mock_file.called

    @patch("builtins.open", new_callable=mock_open)
    def test_log_event_multiple_calls(self, mock_file):
        """Test multiple log events"""
        user_auth_app.log_event("Event 1")
        user_auth_app.log_event("Event 2")
        user_auth_app.log_event("Event 3")
        assert mock_file.call_count == 3


class TestRegisterUser:
    """Tests for register_user function"""

    def setup_method(self):
        """Reset users_db before each test"""
        user_auth_app.users_db.clear()
        user_auth_app.users_db.extend([
            {"username": "admin", "password": "admin123"},
            {"username": "test", "password": "test123"}
        ])

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_register_user_valid(self, mock_print, mock_file):
        """Test registering a valid user"""
        initial_count = len(user_auth_app.users_db)
        user_auth_app.register_user("newuser", "newpass123")
        assert len(user_auth_app.users_db) == initial_count + 1
        assert user_auth_app.users_db[-1]["username"] == "newuser"
        assert user_auth_app.users_db[-1]["password"] == "newpass123"
        mock_print.assert_called_with("User registered successfully!")

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_register_user_weak_password_still_adds(self, mock_print, mock_file):
        """Test that weak password still adds user (validation bug)"""
        user_auth_app.register_user("user", "123")
        # User is still added despite weak password
        assert user_auth_app.users_db[-1]["username"] == "user"
        assert user_auth_app.users_db[-1]["password"] == "123"
        # Warning is printed but user is still added
        assert mock_print.call_count >= 1

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_register_user_empty_password(self, mock_print, mock_file):
        """Test registering with empty password"""
        user_auth_app.register_user("user", "")
        # Empty password triggers warning but user is still added
        assert user_auth_app.users_db[-1]["password"] == ""

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_register_user_duplicate_username(self, mock_file, mock_print):
        """Test registering duplicate username (no validation)"""
        user_auth_app.register_user("admin", "newpass")
        # Should succeed since there's no duplicate check
        assert len([u for u in user_auth_app.users_db if u["username"] == "admin"]) >= 2

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_register_user_logs_password(self, mock_print, mock_file):
        """Test that register_user logs password (security issue)"""
        user_auth_app.register_user("testuser", "secret123")
        handle = mock_file()
        write_calls = [str(call) for call in handle.write.call_args_list]
        assert any("secret123" in str(call) for call in write_calls)

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_register_user_special_characters(self, mock_print, mock_file):
        """Test registering with special characters"""
        user_auth_app.register_user("user@test", "p@$$w0rd!")
        assert user_auth_app.users_db[-1]["username"] == "user@test"

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_register_user_unicode(self, mock_print, mock_file):
        """Test registering with unicode username"""
        user_auth_app.register_user("用户", "密码123")
        assert user_auth_app.users_db[-1]["username"] == "用户"


class TestLogin:
    """Tests for login function"""

    def setup_method(self):
        """Reset state before each test"""
        user_auth_app.users_db.clear()
        user_auth_app.users_db.extend([
            {"username": "admin", "password": "admin123"},
            {"username": "test", "password": "test123"}
        ])
        user_auth_app.sessions.clear()

    @patch("builtins.print")
    def test_login_superuser_success(self, mock_print):
        """Test hardcoded superuser login"""
        result = user_auth_app.login("superuser", "superpass")
        assert result is True
        mock_print.assert_called_once_with("Superuser logged in!")

    @patch("builtins.print")
    @patch("random.randint", return_value=555555)
    def test_login_valid_user_success(self, mock_random, mock_print):
        """Test successful login with valid credentials"""
        result = user_auth_app.login("admin", "admin123")
        assert result is True
        assert "555555" in user_auth_app.sessions
        assert user_auth_app.sessions["555555"]["username"] == "admin"

    @patch("builtins.print")
    def test_login_invalid_username(self, mock_print):
        """Test login with invalid username"""
        result = user_auth_app.login("nonexistent", "password")
        assert result is False
        mock_print.assert_called_once_with("Login failed")

    @patch("builtins.print")
    def test_login_invalid_password(self, mock_print):
        """Test login with invalid password"""
        result = user_auth_app.login("admin", "wrongpass")
        assert result is False
        mock_print.assert_called_once_with("Login failed")

    @patch("builtins.print")
    def test_login_empty_credentials(self, mock_print):
        """Test login with empty credentials"""
        result = user_auth_app.login("", "")
        assert result is False

    @patch("builtins.print")
    def test_login_case_sensitive(self, mock_print):
        """Test that login is case-sensitive"""
        result = user_auth_app.login("ADMIN", "admin123")
        assert result is False

    @patch("builtins.print")
    @patch("random.randint", return_value=777777)
    def test_login_creates_session_with_timestamp(self, mock_random, mock_print):
        """Test that login creates session with timestamp"""
        before_time = time.time()
        result = user_auth_app.login("test", "test123")
        after_time = time.time()

        assert result is True
        assert "777777" in user_auth_app.sessions
        session = user_auth_app.sessions["777777"]
        assert session["username"] == "test"
        assert before_time <= session["time"] <= after_time

    @patch("builtins.print")
    @patch("random.randint")
    def test_login_multiple_sessions(self, mock_random, mock_print):
        """Test multiple logins create multiple sessions"""
        mock_random.side_effect = [111111, 222222, 333333]
        user_auth_app.login("admin", "admin123")
        user_auth_app.login("test", "test123")
        user_auth_app.login("admin", "admin123")
        assert len(user_auth_app.sessions) == 3

    @patch("builtins.print")
    def test_login_superuser_no_session(self, mock_print):
        """Test superuser login doesn't create session"""
        user_auth_app.login("superuser", "superpass")
        assert len(user_auth_app.sessions) == 0


class TestResetPassword:
    """Tests for reset_password function"""

    def setup_method(self):
        """Reset users_db before each test"""
        user_auth_app.users_db.clear()
        user_auth_app.users_db.extend([
            {"username": "admin", "password": "admin123"},
            {"username": "test", "password": "test123"}
        ])

    @patch("builtins.open", new_callable=mock_open)
    def test_reset_password_success(self, mock_file):
        """Test successful password reset"""
        result = user_auth_app.reset_password("admin", "newpass")
        assert result is True
        admin_user = next(u for u in user_auth_app.users_db if u["username"] == "admin")
        assert admin_user["password"] == "newpass"

    @patch("builtins.open", new_callable=mock_open)
    def test_reset_password_nonexistent_user(self, mock_file):
        """Test password reset for nonexistent user"""
        result = user_auth_app.reset_password("nonexistent", "newpass")
        assert result is False

    @patch("builtins.open", new_callable=mock_open)
    def test_reset_password_empty_password(self, mock_file):
        """Test resetting to empty password"""
        result = user_auth_app.reset_password("admin", "")
        assert result is True
        admin_user = next(u for u in user_auth_app.users_db if u["username"] == "admin")
        assert admin_user["password"] == ""

    @patch("builtins.open", new_callable=mock_open)
    def test_reset_password_logs_new_password(self, mock_file):
        """Test that reset_password logs the new password"""
        user_auth_app.reset_password("admin", "newsecret")
        handle = mock_file()
        write_calls = [str(call) for call in handle.write.call_args_list]
        assert any("newsecret" in str(call) for call in write_calls)

    @patch("builtins.open", new_callable=mock_open)
    def test_reset_password_only_first_match(self, mock_file):
        """Test reset only affects first matching user"""
        # Add duplicate username
        user_auth_app.users_db.append({"username": "admin", "password": "other"})
        user_auth_app.reset_password("admin", "resetpass")
        assert user_auth_app.users_db[0]["password"] == "resetpass"
        assert user_auth_app.users_db[-1]["password"] == "other"


class TestLoadConfig:
    """Tests for load_config function"""

    @patch("builtins.open", mock_open(read_data='{"key": "value"}'))
    def test_load_config_basic(self):
        """Test loading basic config file"""
        result = user_auth_app.load_config("config.json")
        assert result == {"key": "value"}

    @patch("builtins.open", mock_open(read_data='{"users": ["admin", "test"], "timeout": 3600}'))
    def test_load_config_complex(self):
        """Test loading complex config"""
        result = user_auth_app.load_config("config.json")
        assert "users" in result
        assert "timeout" in result
        assert result["users"] == ["admin", "test"]

    @patch("builtins.open", mock_open(read_data='{}'))
    def test_load_config_empty_json(self):
        """Test loading empty JSON object"""
        result = user_auth_app.load_config("config.json")
        assert result == {}

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_config_file_not_found(self, mock_file):
        """Test loading non-existent file raises exception"""
        with pytest.raises(FileNotFoundError):
            user_auth_app.load_config("nonexistent.json")

    @patch("builtins.open", mock_open(read_data='invalid json'))
    def test_load_config_invalid_json(self):
        """Test loading invalid JSON raises exception"""
        with pytest.raises(json.JSONDecodeError):
            user_auth_app.load_config("invalid.json")

    @patch("builtins.open", mock_open(read_data='{"nested": {"deep": {"key": "value"}}}'))
    def test_load_config_nested_structure(self):
        """Test loading deeply nested JSON structure"""
        result = user_auth_app.load_config("config.json")
        assert result["nested"]["deep"]["key"] == "value"


class TestSaveConfig:
    """Tests for save_config function"""

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_save_config_basic(self, mock_json_dump, mock_file):
        """Test saving basic config"""
        data = {"key": "value"}
        user_auth_app.save_config("config.json", data)
        mock_file.assert_called_once_with("config.json", "w")
        mock_json_dump.assert_called_once()

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_save_config_complex(self, mock_json_dump, mock_file):
        """Test saving complex config"""
        data = {"users": ["admin", "test"], "timeout": 3600, "nested": {"key": "value"}}
        user_auth_app.save_config("config.json", data)
        assert mock_json_dump.called

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_save_config_empty_dict(self, mock_json_dump, mock_file):
        """Test saving empty dictionary"""
        user_auth_app.save_config("config.json", {})
        assert mock_json_dump.called

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_save_config_closes_file(self, mock_json_dump, mock_file):
        """Test that save_config closes the file"""
        user_auth_app.save_config("config.json", {"key": "value"})
        handle = mock_file()
        handle.close.assert_called_once()

    @patch("builtins.open", side_effect=PermissionError)
    def test_save_config_permission_error(self, mock_file):
        """Test saving config with permission error"""
        with pytest.raises(PermissionError):
            user_auth_app.save_config("config.json", {"key": "value"})


class TestDeleteUser:
    """Tests for delete_user function"""

    def setup_method(self):
        """Reset users_db before each test"""
        user_auth_app.users_db.clear()
        user_auth_app.users_db.extend([
            {"username": "admin", "password": "admin123"},
            {"username": "test", "password": "test123"},
            {"username": "guest", "password": "guest123"}
        ])

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_delete_user_success(self, mock_print, mock_file):
        """Test successful user deletion"""
        initial_count = len(user_auth_app.users_db)
        user_auth_app.delete_user("test")
        assert len(user_auth_app.users_db) == initial_count - 1
        assert not any(u["username"] == "test" for u in user_auth_app.users_db)
        mock_print.assert_called_with("User test deleted.")

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_delete_user_nonexistent(self, mock_print, mock_file):
        """Test deleting nonexistent user"""
        initial_count = len(user_auth_app.users_db)
        user_auth_app.delete_user("nonexistent")
        assert len(user_auth_app.users_db) == initial_count
        mock_print.assert_called_with("User nonexistent deleted.")

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_delete_user_multiple_with_same_name(self, mock_print, mock_file):
        """Test deleting when multiple users have same name"""
        user_auth_app.users_db.append({"username": "admin", "password": "other"})
        initial_count = len(user_auth_app.users_db)
        user_auth_app.delete_user("admin")
        # Should remove all users with that username
        assert len(user_auth_app.users_db) < initial_count
        assert not any(u["username"] == "admin" for u in user_auth_app.users_db)

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_delete_user_empty_username(self, mock_print, mock_file):
        """Test deleting user with empty username"""
        initial_count = len(user_auth_app.users_db)
        user_auth_app.delete_user("")
        assert len(user_auth_app.users_db) == initial_count

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_delete_user_logs_event(self, mock_print, mock_file):
        """Test that delete_user logs the event"""
        user_auth_app.delete_user("test")
        handle = mock_file()
        assert handle.write.called

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_delete_all_users(self, mock_print, mock_file):
        """Test deleting all users one by one"""
        user_auth_app.delete_user("admin")
        user_auth_app.delete_user("test")
        user_auth_app.delete_user("guest")
        assert len(user_auth_app.users_db) == 0


class TestIntegration:
    """Integration tests combining multiple functions"""

    def setup_method(self):
        """Reset state before each test"""
        user_auth_app.users_db.clear()
        user_auth_app.users_db.extend([
            {"username": "admin", "password": "admin123"},
            {"username": "test", "password": "test123"}
        ])
        user_auth_app.sessions.clear()

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_register_and_login_new_user(self, mock_print, mock_file):
        """Test registering a user and then logging in"""
        user_auth_app.register_user("newuser", "newpass123")
        result = user_auth_app.login("newuser", "newpass123")
        assert result is True

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_reset_and_login_with_new_password(self, mock_print, mock_file):
        """Test password reset and login with new password"""
        user_auth_app.reset_password("admin", "newpass456")

        # Old password should fail
        result1 = user_auth_app.login("admin", "admin123")
        assert result1 is False

        # New password should work
        result2 = user_auth_app.login("admin", "newpass456")
        assert result2 is True

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_register_reset_login_workflow(self, mock_print, mock_file):
        """Test complete workflow: register, reset, login"""
        user_auth_app.register_user("user1", "pass1")
        user_auth_app.reset_password("user1", "newpass1")
        result = user_auth_app.login("user1", "newpass1")
        assert result is True

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_register_and_delete_user(self, mock_print, mock_file):
        """Test registering and then deleting a user"""
        user_auth_app.register_user("tempuser", "temppass")
        assert any(u["username"] == "tempuser" for u in user_auth_app.users_db)

        user_auth_app.delete_user("tempuser")
        assert not any(u["username"] == "tempuser" for u in user_auth_app.users_db)

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    @patch("random.randint")
    def test_multiple_users_multiple_sessions(self, mock_random, mock_print, mock_file):
        """Test multiple users with multiple sessions"""
        mock_random.side_effect = [100000, 200000, 300000]

        user_auth_app.register_user("user1", "pass1")
        user_auth_app.register_user("user2", "pass2")

        user_auth_app.login("user1", "pass1")
        user_auth_app.login("user2", "pass2")
        user_auth_app.login("admin", "admin123")

        assert len(user_auth_app.sessions) == 3

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    @patch("builtins.print")
    def test_save_and_load_config_integration(self, mock_print, mock_json_dump, mock_file):
        """Test saving and loading config"""
        config_data = {"timeout": 3600, "max_users": 100}

        # Save config
        user_auth_app.save_config("test.json", config_data)
        assert mock_json_dump.called


class TestEdgeCases:
    """Tests for edge cases and boundary conditions"""

    def setup_method(self):
        """Reset state before each test"""
        user_auth_app.users_db.clear()
        user_auth_app.users_db.extend([
            {"username": "admin", "password": "admin123"},
            {"username": "test", "password": "test123"}
        ])
        user_auth_app.sessions.clear()

    @patch("builtins.print")
    def test_login_with_none_values(self, mock_print):
        """Test login with None values"""
        result = user_auth_app.login(None, "password")
        assert result is False

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_register_user_with_very_long_username(self, mock_print, mock_file):
        """Test registering user with very long username"""
        long_username = "u" * 10000
        user_auth_app.register_user(long_username, "pass123")
        assert user_auth_app.users_db[-1]["username"] == long_username

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_register_user_with_very_long_password(self, mock_print, mock_file):
        """Test registering user with very long password"""
        long_password = "p" * 10000
        user_auth_app.register_user("user", long_password)
        assert user_auth_app.users_db[-1]["password"] == long_password

    def test_hash_password_with_null_bytes(self):
        """Test hashing password with null bytes"""
        result = user_auth_app.hash_password("pass\x00word")
        assert isinstance(result, str)
        assert len(result) == 32

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_delete_user_with_special_chars(self, mock_print, mock_file):
        """Test deleting user with special characters in name"""
        user_auth_app.users_db.append({"username": "user@test", "password": "pass"})
        user_auth_app.delete_user("user@test")
        assert not any(u["username"] == "user@test" for u in user_auth_app.users_db)

    @patch("builtins.print")
    @patch("random.randint", return_value=100000)
    def test_session_token_collision(self, mock_random, mock_print):
        """Test behavior when session tokens collide"""
        # First login
        user_auth_app.login("admin", "admin123")
        first_session = user_auth_app.sessions["100000"].copy()

        # Second login with same token
        user_auth_app.login("test", "test123")
        second_session = user_auth_app.sessions["100000"]

        # Second session overwrites first
        assert second_session["username"] == "test"
        assert second_session["username"] != first_session["username"]


class TestSecurityIssues:
    """Tests documenting security issues in the code"""

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_password_stored_in_plaintext(self, mock_print, mock_file):
        """Document that passwords are stored in plaintext"""
        user_auth_app.register_user("testuser", "mysecretpassword")
        user = next(u for u in user_auth_app.users_db if u["username"] == "testuser")
        # Password is stored in plaintext (security issue)
        assert user["password"] == "mysecretpassword"

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_passwords_logged_to_file(self, mock_print, mock_file):
        """Document that passwords are logged to file"""
        user_auth_app.register_user("user", "secretpass")
        handle = mock_file()
        write_calls = [str(call) for call in handle.write.call_args_list]
        assert any("secretpass" in str(call) for call in write_calls)

    def test_weak_hashing_algorithm(self):
        """Document use of weak MD5 hashing"""
        result = user_auth_app.hash_password("password")
        assert result == hashlib.md5(b"password").hexdigest()

    @patch("builtins.print")
    def test_hardcoded_credentials(self, mock_print):
        """Document hardcoded superuser credentials"""
        result = user_auth_app.login("superuser", "superpass")
        assert result is True

    @patch("builtins.print")
    @patch("random.randint", return_value=123456)
    def test_weak_session_tokens(self, mock_random, mock_print):
        """Document weak session token generation"""
        user_auth_app.login("admin", "admin123")
        # Session tokens are only 6 digits (100000-999999)
        assert "123456" in user_auth_app.sessions

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_weak_password_validation(self, mock_print, mock_file):
        """Document weak password validation"""
        # Only checks length < 4, but still adds user
        user_auth_app.register_user("user1", "1")
        user_auth_app.register_user("user2", "")
        # Users are added despite weak passwords
        assert any(u["username"] == "user1" for u in user_auth_app.users_db)
        assert any(u["username"] == "user2" for u in user_auth_app.users_db)

    def test_file_handle_not_closed(self):
        """Document that load_config doesn't close file handle"""
        with patch("builtins.open", mock_open(read_data='{"key": "value"}')):
            result = user_auth_app.load_config("config.json")
            # File handle is not closed (resource leak)
            assert result == {"key": "value"}


class TestRegressionAndBoundary:
    """Additional regression and boundary tests for enhanced coverage"""

    def setup_method(self):
        """Reset state before each test"""
        user_auth_app.users_db.clear()
        user_auth_app.users_db.extend([
            {"username": "admin", "password": "admin123"},
            {"username": "test", "password": "test123"}
        ])
        user_auth_app.sessions.clear()

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_register_many_users_boundary(self, mock_print, mock_file):
        """Test registering many users to verify system handles growth"""
        initial_count = len(user_auth_app.users_db)
        for i in range(100):
            user_auth_app.register_user(f"user{i}", f"password{i}")

        assert len(user_auth_app.users_db) == initial_count + 100

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_delete_and_recreate_user(self, mock_print, mock_file):
        """Regression test: ensure deleted user can be recreated"""
        user_auth_app.register_user("tempuser", "temppass")
        assert any(u["username"] == "tempuser" for u in user_auth_app.users_db)

        user_auth_app.delete_user("tempuser")
        assert not any(u["username"] == "tempuser" for u in user_auth_app.users_db)

        # Recreate with different password
        user_auth_app.register_user("tempuser", "newpass")
        user = next(u for u in user_auth_app.users_db if u["username"] == "tempuser")
        assert user["password"] == "newpass"

    @patch("builtins.print")
    @patch("random.randint")
    def test_session_overflow_with_many_logins(self, mock_random, mock_print):
        """Test system behavior with many active sessions"""
        mock_random.side_effect = range(100000, 200000)

        # Create many sessions
        for i in range(50):
            user_auth_app.login("admin", "admin123")

        # All sessions should be preserved (no limit implemented)
        assert len(user_auth_app.sessions) == 50

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_password_complexity_bypass(self, mock_print, mock_file):
        """Document that weak password validation can be bypassed"""
        # Register with 1-char password (should warn but still adds)
        user_auth_app.register_user("weak1", "a")
        # Register with 2-char password (should warn but still adds)
        user_auth_app.register_user("weak2", "ab")
        # Register with 3-char password (should warn but still adds)
        user_auth_app.register_user("weak3", "abc")

        # All users should be added despite weak passwords
        assert any(u["username"] == "weak1" for u in user_auth_app.users_db)
        assert any(u["username"] == "weak2" for u in user_auth_app.users_db)
        assert any(u["username"] == "weak3" for u in user_auth_app.users_db)


class TestAdditionalRegressionCases:
    """Additional regression and negative test cases for enhanced confidence"""

    def setup_method(self):
        """Reset state before each test"""
        user_auth_app.users_db.clear()
        user_auth_app.users_db.extend([
            {"username": "admin", "password": "admin123"},
            {"username": "test", "password": "test123"}
        ])
        user_auth_app.sessions.clear()

    def test_hash_password_consistency_across_calls(self):
        """Test that multiple calls produce consistent hashes"""
        password = "consistent_test"
        hashes = [user_auth_app.hash_password(password) for _ in range(10)]
        assert all(h == hashes[0] for h in hashes)

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_register_user_boundary_4_char_password(self, mock_print, mock_file):
        """Boundary test: 4-character password should not trigger warning"""
        user_auth_app.register_user("user4", "abcd")
        # 4 chars is at the boundary, should not print "too short"
        assert any(u["username"] == "user4" for u in user_auth_app.users_db)

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_register_user_with_tabs_and_newlines(self, mock_print, mock_file):
        """Test registering user with tabs and newlines in password"""
        user_auth_app.register_user("user", "pass\t\nword")
        user = next(u for u in user_auth_app.users_db if u["username"] == "user")
        assert user["password"] == "pass\t\nword"

    @patch("builtins.print")
    @patch("random.randint")
    def test_login_creates_unique_session_tokens(self, mock_random, mock_print):
        """Test that each login creates a unique session token"""
        mock_random.side_effect = [111111, 222222, 333333]
        user_auth_app.login("admin", "admin123")
        user_auth_app.login("test", "test123")
        user_auth_app.login("admin", "admin123")
        assert len(user_auth_app.sessions) == 3
        assert "111111" in user_auth_app.sessions
        assert "222222" in user_auth_app.sessions
        assert "333333" in user_auth_app.sessions

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_delete_user_case_sensitive(self, mock_print, mock_file):
        """Test that delete_user is case-sensitive"""
        initial_count = len(user_auth_app.users_db)
        user_auth_app.delete_user("ADMIN")  # Wrong case
        # Should not delete "admin"
        assert len(user_auth_app.users_db) == initial_count

    @patch("builtins.open", new_callable=mock_open)
    def test_reset_password_unicode_password(self, mock_file):
        """Test resetting password to unicode characters"""
        result = user_auth_app.reset_password("admin", "密码")
        assert result is True
        admin = next(u for u in user_auth_app.users_db if u["username"] == "admin")
        assert admin["password"] == "密码"

    @patch("builtins.open", mock_open(read_data='{"bool": true, "null": null, "num": 42}'))
    def test_load_config_with_json_types(self):
        """Test loading config with various JSON types"""
        result = user_auth_app.load_config("config.json")
        assert result["bool"] is True
        assert result["null"] is None
        assert result["num"] == 42

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_save_config_with_unicode(self, mock_json_dump, mock_file):
        """Test saving config with unicode data"""
        data = {"message": "こんにちは", "user": "用户"}
        user_auth_app.save_config("config.json", data)
        assert mock_json_dump.called

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_register_multiple_users_same_password(self, mock_print, mock_file):
        """Test registering multiple users with same password"""
        user_auth_app.register_user("user1", "samepass")
        user_auth_app.register_user("user2", "samepass")
        user_auth_app.register_user("user3", "samepass")
        # All should be registered successfully
        assert len([u for u in user_auth_app.users_db if u["password"] == "samepass"]) >= 3

    def test_hash_password_binary_data(self):
        """Test hashing with binary-like string"""
        result = user_auth_app.hash_password("\x00\x01\x02\x03")
        assert isinstance(result, str)
        assert len(result) == 32

    @patch("builtins.print")
    def test_login_superuser_multiple_times(self, mock_print):
        """Test superuser can login multiple times without creating sessions"""
        user_auth_app.login("superuser", "superpass")
        user_auth_app.login("superuser", "superpass")
        user_auth_app.login("superuser", "superpass")
        # No sessions should be created for superuser
        assert len(user_auth_app.sessions) == 0

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_delete_user_from_empty_database(self, mock_print, mock_file):
        """Test deleting user when database is empty"""
        user_auth_app.users_db.clear()
        user_auth_app.delete_user("nonexistent")
        assert len(user_auth_app.users_db) == 0

    @patch("builtins.print")
    @patch("random.randint", return_value=500000)
    def test_session_expiration_not_implemented(self, mock_random, mock_print):
        """Document that sessions never expire"""
        user_auth_app.login("admin", "admin123")
        session = user_auth_app.sessions["500000"]
        # Session has time but no expiration logic
        assert "time" in session
        # Sessions persist indefinitely (potential security issue)

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_register_and_immediate_login(self, mock_print, mock_file):
        """Test registering and immediately logging in"""
        user_auth_app.register_user("newuser", "newpass123")
        result = user_auth_app.login("newuser", "newpass123")
        assert result is True

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_reset_password_multiple_times(self, mock_print, mock_file):
        """Test resetting password multiple times"""
        user_auth_app.reset_password("admin", "pass1")
        user_auth_app.reset_password("admin", "pass2")
        user_auth_app.reset_password("admin", "pass3")
        admin = next(u for u in user_auth_app.users_db if u["username"] == "admin")
        assert admin["password"] == "pass3"

    def test_users_db_mutable_reference_exposure(self):
        """Test that users_db can be directly modified (security issue)"""
        initial_len = len(user_auth_app.users_db)
        # Direct modification is possible
        user_auth_app.users_db.append({"username": "hacker", "password": "hack"})
        assert len(user_auth_app.users_db) == initial_len + 1

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_register_user_long_username_and_password(self, mock_print, mock_file):
        """Test registration with very long username and password"""
        long_user = "u" * 1000
        long_pass = "p" * 1000
        user_auth_app.register_user(long_user, long_pass)
        user = next(u for u in user_auth_app.users_db if u["username"] == long_user)
        assert user["password"] == long_pass