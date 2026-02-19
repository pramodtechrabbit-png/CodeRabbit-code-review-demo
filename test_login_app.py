"""
Comprehensive test suite for login_app.py
Tests cover main functionality, edge cases, security issues, and error handling.
"""

import pytest
import os
import json
import hashlib
import time
from unittest.mock import patch, mock_open, MagicMock
import login_app


class TestHashPassword:
    """Tests for hash_password function"""

    def test_hash_password_basic(self):
        """Test basic password hashing"""
        result = login_app.hash_password("password123")
        assert isinstance(result, str)
        assert len(result) == 32  # MD5 produces 32-char hex string

    def test_hash_password_consistency(self):
        """Test that same password produces same hash"""
        hash1 = login_app.hash_password("test123")
        hash2 = login_app.hash_password("test123")
        assert hash1 == hash2

    def test_hash_password_different_inputs(self):
        """Test that different passwords produce different hashes"""
        hash1 = login_app.hash_password("password1")
        hash2 = login_app.hash_password("password2")
        assert hash1 != hash2

    def test_hash_password_empty_string(self):
        """Test hashing empty string"""
        result = login_app.hash_password("")
        expected = hashlib.md5(b"").hexdigest()
        assert result == expected

    def test_hash_password_unicode(self):
        """Test hashing unicode characters"""
        result = login_app.hash_password("пароль日本語")
        assert isinstance(result, str)
        assert len(result) == 32

    def test_hash_password_special_chars(self):
        """Test hashing with special characters"""
        result = login_app.hash_password("p@$$w0rd!#%")
        assert isinstance(result, str)
        assert len(result) == 32

    def test_hash_password_long_input(self):
        """Test hashing very long password"""
        long_password = "a" * 10000
        result = login_app.hash_password(long_password)
        assert len(result) == 32


class TestLog:
    """Tests for log function"""

    @patch("builtins.open", new_callable=mock_open)
    @patch("time.ctime", return_value="Wed Jan 1 00:00:00 2025")
    def test_log_writes_message(self, mock_ctime, mock_file):
        """Test that log writes formatted message"""
        login_app.log("Test message")
        mock_file.assert_called_once_with("login.log", "a")
        handle = mock_file()
        handle.write.assert_called_once_with("Wed Jan 1 00:00:00 2025 - Test message\n")

    @patch("builtins.open", new_callable=mock_open)
    def test_log_empty_message(self, mock_file):
        """Test logging empty message"""
        login_app.log("")
        handle = mock_file()
        assert handle.write.called

    @patch("builtins.open", new_callable=mock_open)
    def test_log_unicode_message(self, mock_file):
        """Test logging unicode characters"""
        login_app.log("User 日本語 logged in")
        assert mock_file.called


class TestAddUser:
    """Tests for add_user function"""

    def setup_method(self):
        """Reset USERS list before each test"""
        login_app.USERS.clear()
        login_app.USERS.extend([
            {"username": "admin", "password": "1234"},
            {"username": "guest", "password": "guest"}
        ])

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_add_user_basic(self, mock_print, mock_file):
        """Test adding a new user"""
        initial_count = len(login_app.USERS)
        login_app.add_user("testuser", "testpass")
        assert len(login_app.USERS) == initial_count + 1
        assert login_app.USERS[-1]["username"] == "testuser"
        assert login_app.USERS[-1]["password"] == "testpass"
        mock_print.assert_called_once_with("User added!")

    @patch("builtins.open", new_callable=mock_open)
    def test_add_user_duplicate_username(self, mock_file):
        """Test adding user with duplicate username (no validation)"""
        login_app.add_user("admin", "newpass")
        # Should succeed since there's no duplicate check
        assert len([u for u in login_app.USERS if u["username"] == "admin"]) >= 2

    @patch("builtins.open", new_callable=mock_open)
    def test_add_user_empty_username(self, mock_file):
        """Test adding user with empty username"""
        login_app.add_user("", "password")
        assert login_app.USERS[-1]["username"] == ""

    @patch("builtins.open", new_callable=mock_open)
    def test_add_user_empty_password(self, mock_file):
        """Test adding user with empty password"""
        login_app.add_user("user", "")
        assert login_app.USERS[-1]["password"] == ""

    @patch("builtins.open", new_callable=mock_open)
    def test_add_user_special_chars(self, mock_file):
        """Test adding user with special characters"""
        login_app.add_user("user@test", "p@$$w0rd!")
        assert login_app.USERS[-1]["username"] == "user@test"

    @patch("builtins.open", new_callable=mock_open)
    def test_add_user_logs_password(self, mock_file):
        """Test that add_user logs password (security issue)"""
        login_app.add_user("testuser", "secret123")
        handle = mock_file()
        # Verify that write was called with password in message
        write_calls = [str(call) for call in handle.write.call_args_list]
        assert any("secret123" in str(call) for call in write_calls)


class TestLogin:
    """Tests for login function"""

    def setup_method(self):
        """Reset USERS and SESSIONS before each test"""
        login_app.USERS.clear()
        login_app.USERS.extend([
            {"username": "admin", "password": "1234"},
            {"username": "guest", "password": "guest"}
        ])
        login_app.SESSIONS.clear()

    @patch("builtins.print")
    def test_login_superadmin_success(self, mock_print):
        """Test hardcoded superadmin login"""
        result = login_app.login("superadmin", "super123")
        assert result is True
        mock_print.assert_called_once_with("Login successful (superadmin)")

    @patch("builtins.print")
    @patch("random.randint", return_value=5555)
    def test_login_valid_user_success(self, mock_random, mock_print):
        """Test successful login with valid credentials"""
        result = login_app.login("admin", "1234")
        assert result is True
        assert "5555" in login_app.SESSIONS
        assert login_app.SESSIONS["5555"]["username"] == "admin"

    @patch("builtins.print")
    def test_login_invalid_username(self, mock_print):
        """Test login with invalid username"""
        result = login_app.login("nonexistent", "password")
        assert result is False
        mock_print.assert_called_once_with("Login failed")

    @patch("builtins.print")
    def test_login_invalid_password(self, mock_print):
        """Test login with invalid password"""
        result = login_app.login("admin", "wrongpass")
        assert result is False
        mock_print.assert_called_once_with("Login failed")

    @patch("builtins.print")
    def test_login_empty_credentials(self, mock_print):
        """Test login with empty credentials"""
        result = login_app.login("", "")
        assert result is False

    @patch("builtins.print")
    def test_login_case_sensitive(self, mock_print):
        """Test that login is case-sensitive"""
        result = login_app.login("ADMIN", "1234")
        assert result is False

    @patch("builtins.print")
    @patch("random.randint", return_value=7777)
    def test_login_creates_session(self, mock_random, mock_print):
        """Test that login creates session with timestamp"""
        before_time = time.time()
        result = login_app.login("guest", "guest")
        after_time = time.time()

        assert result is True
        assert "7777" in login_app.SESSIONS
        session = login_app.SESSIONS["7777"]
        assert session["username"] == "guest"
        assert before_time <= session["time"] <= after_time

    @patch("builtins.print")
    def test_login_superadmin_priority(self, mock_print):
        """Test superadmin check happens before regular users"""
        # Add a regular user with same credentials
        login_app.USERS.append({"username": "superadmin", "password": "wrongpass"})
        result = login_app.login("superadmin", "super123")
        assert result is True
        # Should not create session for superadmin
        assert len(login_app.SESSIONS) == 0

    @patch("builtins.print")
    @patch("random.randint")
    def test_login_multiple_sessions(self, mock_random, mock_print):
        """Test multiple logins create multiple sessions"""
        mock_random.side_effect = [1111, 2222, 3333]
        login_app.login("admin", "1234")
        login_app.login("guest", "guest")
        login_app.login("admin", "1234")
        assert len(login_app.SESSIONS) == 3


class TestResetPassword:
    """Tests for reset_password function"""

    def setup_method(self):
        """Reset USERS before each test"""
        login_app.USERS.clear()
        login_app.USERS.extend([
            {"username": "admin", "password": "1234"},
            {"username": "guest", "password": "guest"}
        ])

    @patch("builtins.open", new_callable=mock_open)
    def test_reset_password_success(self, mock_file):
        """Test successful password reset"""
        result = login_app.reset_password("admin", "newpass")
        assert result is True
        admin_user = next(u for u in login_app.USERS if u["username"] == "admin")
        assert admin_user["password"] == "newpass"

    @patch("builtins.open", new_callable=mock_open)
    def test_reset_password_nonexistent_user(self, mock_file):
        """Test password reset for nonexistent user"""
        result = login_app.reset_password("nonexistent", "newpass")
        assert result is False

    @patch("builtins.open", new_callable=mock_open)
    def test_reset_password_empty_password(self, mock_file):
        """Test resetting to empty password"""
        result = login_app.reset_password("admin", "")
        assert result is True
        admin_user = next(u for u in login_app.USERS if u["username"] == "admin")
        assert admin_user["password"] == ""

    @patch("builtins.open", new_callable=mock_open)
    def test_reset_password_logs_new_password(self, mock_file):
        """Test that reset_password logs the operation"""
        login_app.reset_password("admin", "newsecret")
        handle = mock_file()
        assert handle.write.called

    @patch("builtins.open", new_callable=mock_open)
    def test_reset_password_multiple_users(self, mock_file):
        """Test reset only affects specified user"""
        original_guest_pass = login_app.USERS[1]["password"]
        login_app.reset_password("admin", "newpass")
        assert login_app.USERS[1]["password"] == original_guest_pass


class TestReadConfig:
    """Tests for read_config function"""

    @patch("builtins.open", mock_open(read_data='{"key": "value"}'))
    def test_read_config_basic(self):
        """Test reading basic config file"""
        result = login_app.read_config("config.json")
        assert result == {"key": "value"}

    @patch("builtins.open", mock_open(read_data='{"users": ["admin", "guest"], "timeout": 3600}'))
    def test_read_config_complex(self):
        """Test reading complex config"""
        result = login_app.read_config("config.json")
        assert "users" in result
        assert "timeout" in result
        assert result["users"] == ["admin", "guest"]

    @patch("builtins.open", mock_open(read_data='{}'))
    def test_read_config_empty_json(self):
        """Test reading empty JSON object"""
        result = login_app.read_config("config.json")
        assert result == {}

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_read_config_file_not_found(self, mock_file):
        """Test reading non-existent file raises exception"""
        with pytest.raises(FileNotFoundError):
            login_app.read_config("nonexistent.json")

    @patch("builtins.open", mock_open(read_data='invalid json'))
    def test_read_config_invalid_json(self):
        """Test reading invalid JSON raises exception"""
        with pytest.raises(json.JSONDecodeError):
            login_app.read_config("invalid.json")

    @patch("builtins.open", mock_open(read_data='{"nested": {"key": "value"}}'))
    def test_read_config_nested_structure(self):
        """Test reading nested JSON structure"""
        result = login_app.read_config("config.json")
        assert result["nested"]["key"] == "value"


class TestIntegration:
    """Integration tests combining multiple functions"""

    def setup_method(self):
        """Reset state before each test"""
        login_app.USERS.clear()
        login_app.USERS.extend([
            {"username": "admin", "password": "1234"},
            {"username": "guest", "password": "guest"}
        ])
        login_app.SESSIONS.clear()

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_add_and_login_new_user(self, mock_print, mock_file):
        """Test adding a user and then logging in"""
        login_app.add_user("newuser", "newpass")
        result = login_app.login("newuser", "newpass")
        assert result is True

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_reset_and_login_with_new_password(self, mock_print, mock_file):
        """Test password reset and login with new password"""
        login_app.reset_password("admin", "newpass123")

        # Old password should fail
        result1 = login_app.login("admin", "1234")
        assert result1 is False

        # New password should work
        result2 = login_app.login("admin", "newpass123")
        assert result2 is True

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    @patch("random.randint")
    def test_multiple_users_multiple_sessions(self, mock_random, mock_print, mock_file):
        """Test multiple users with multiple sessions"""
        mock_random.side_effect = [1000, 2000, 3000]

        login_app.add_user("user1", "pass1")
        login_app.add_user("user2", "pass2")

        login_app.login("user1", "pass1")
        login_app.login("user2", "pass2")
        login_app.login("admin", "1234")

        assert len(login_app.SESSIONS) == 3
        assert "1000" in login_app.SESSIONS
        assert "2000" in login_app.SESSIONS
        assert "3000" in login_app.SESSIONS


class TestEdgeCases:
    """Tests for edge cases and boundary conditions"""

    def setup_method(self):
        """Reset state before each test"""
        login_app.USERS.clear()
        login_app.USERS.extend([
            {"username": "admin", "password": "1234"},
            {"username": "guest", "password": "guest"}
        ])
        login_app.SESSIONS.clear()

    @patch("builtins.print")
    def test_login_with_none_username(self, mock_print):
        """Test login with None as username"""
        result = login_app.login(None, "password")
        assert result is False

    @patch("builtins.print")
    def test_login_with_none_password(self, mock_print):
        """Test login with None as password"""
        # login function handles None gracefully, returns False
        result = login_app.login("admin", None)
        assert result is False

    @patch("builtins.open", new_callable=mock_open)
    def test_add_user_with_very_long_username(self, mock_file):
        """Test adding user with very long username"""
        long_username = "u" * 10000
        login_app.add_user(long_username, "pass")
        assert login_app.USERS[-1]["username"] == long_username

    @patch("builtins.open", new_callable=mock_open)
    def test_add_user_with_very_long_password(self, mock_file):
        """Test adding user with very long password"""
        long_password = "p" * 10000
        login_app.add_user("user", long_password)
        assert login_app.USERS[-1]["password"] == long_password

    def test_hash_password_with_null_bytes(self):
        """Test hashing password with null bytes"""
        result = login_app.hash_password("pass\x00word")
        assert isinstance(result, str)
        assert len(result) == 32

    @patch("builtins.print")
    def test_login_with_sql_injection_attempt(self, mock_print):
        """Test login with SQL injection string (no SQL, but test string handling)"""
        result = login_app.login("admin' OR '1'='1", "password")
        assert result is False

    @patch("builtins.open", new_callable=mock_open)
    def test_reset_password_first_user_only(self, mock_file):
        """Test that reset_password only resets first matching user"""
        # Add duplicate username
        login_app.USERS.append({"username": "admin", "password": "other"})
        login_app.reset_password("admin", "resetpass")

        # Check first admin is reset
        assert login_app.USERS[0]["password"] == "resetpass"
        # Second admin should be unchanged
        assert login_app.USERS[-1]["password"] == "other"


class TestSecurityIssues:
    """Tests documenting security issues in the code"""

    @patch("builtins.open", new_callable=mock_open)
    def test_password_stored_in_plaintext(self, mock_file):
        """Document that passwords are stored in plaintext"""
        login_app.add_user("testuser", "mysecretpassword")
        user = next(u for u in login_app.USERS if u["username"] == "testuser")
        # Password is stored in plaintext (security issue)
        assert user["password"] == "mysecretpassword"

    @patch("builtins.open", new_callable=mock_open)
    def test_passwords_logged_to_file(self, mock_file):
        """Document that passwords are logged to file"""
        login_app.add_user("user", "secretpass")
        handle = mock_file()
        # Verify password appears in log
        write_calls = [str(call) for call in handle.write.call_args_list]
        assert any("secretpass" in str(call) for call in write_calls)

    def test_weak_hashing_algorithm(self):
        """Document use of weak MD5 hashing"""
        # MD5 is cryptographically broken
        result = login_app.hash_password("password")
        # MD5 hash is predictable and crackable
        assert result == hashlib.md5(b"password").hexdigest()

    @patch("builtins.print")
    def test_hardcoded_credentials(self, mock_print):
        """Document hardcoded superadmin credentials"""
        # Hardcoded credentials are a security risk
        result = login_app.login("superadmin", "super123")
        assert result is True

    @patch("builtins.print")
    @patch("random.randint", return_value=1234)
    def test_weak_session_tokens(self, mock_random, mock_print):
        """Document weak session token generation"""
        # Ensure USERS has admin with password "1234"
        login_app.USERS.clear()
        login_app.USERS.append({"username": "admin", "password": "1234"})
        login_app.login("admin", "1234")
        # Session tokens are only 4 digits (1000-9999), easily guessable
        assert "1234" in login_app.SESSIONS

    def test_no_password_strength_requirements(self):
        """Document lack of password strength requirements"""
        # Weak passwords are accepted
        with patch("builtins.open", mock_open()):
            login_app.add_user("user", "1")
            login_app.add_user("user2", "")
            # No validation occurs
            assert True


class TestRegressionAndBoundary:
    """Additional regression and boundary tests for enhanced coverage"""

    def setup_method(self):
        """Reset state before each test"""
        login_app.USERS.clear()
        login_app.USERS.extend([
            {"username": "admin", "password": "1234"},
            {"username": "guest", "password": "guest"}
        ])
        login_app.SESSIONS.clear()

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    @patch("random.randint")
    def test_concurrent_login_attempts_different_users(self, mock_random, mock_print, mock_file):
        """Test multiple concurrent login attempts create separate sessions"""
        mock_random.side_effect = [1111, 2222, 3333, 4444, 5555]

        # Simulate multiple users logging in
        login_app.login("admin", "1234")
        login_app.login("guest", "guest")
        login_app.login("admin", "1234")  # Same user, new session
        login_app.login("guest", "guest")  # Same user, new session

        # All sessions should be preserved
        assert len(login_app.SESSIONS) == 4
        assert "1111" in login_app.SESSIONS
        assert "2222" in login_app.SESSIONS
        assert "3333" in login_app.SESSIONS
        assert "4444" in login_app.SESSIONS

    @patch("builtins.open", new_callable=mock_open)
    def test_user_list_boundary_many_users(self, mock_file):
        """Test adding many users to verify list handles growth"""
        initial_count = len(login_app.USERS)
        for i in range(100):
            login_app.add_user(f"user{i}", f"pass{i}")

        assert len(login_app.USERS) == initial_count + 100

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_password_reset_regression(self, mock_print, mock_file):
        """Regression test: ensure reset doesn't affect other users"""
        original_guest_password = "guest"

        # Reset admin password
        login_app.reset_password("admin", "newadminpass")

        # Verify admin password changed
        assert any(u["username"] == "admin" and u["password"] == "newadminpass"
                  for u in login_app.USERS)

        # Verify guest password unchanged
        assert any(u["username"] == "guest" and u["password"] == original_guest_password
                  for u in login_app.USERS)

    @patch("builtins.print")
    def test_login_timing_attack_vulnerability(self, mock_print):
        """Document potential timing attack vulnerability"""
        # Both should take similar time but function doesn't have constant-time comparison
        result1 = login_app.login("admin", "1234")
        result2 = login_app.login("nonexistent", "1234")

        assert result1 is True
        assert result2 is False
        # In production, timing differences could reveal valid usernames

    @patch("builtins.print")
    @patch("random.randint")
    def test_session_token_predictability_and_collision(self, mock_random, mock_print):
        """Regression test: Document session token collision and predictability issues"""
        login_app.SESSIONS.clear()

        # Tokens are only 4 digits (1000-9999), highly predictable
        mock_random.return_value = 5000
        login_app.login("admin", "1234")
        assert "5000" in login_app.SESSIONS

        # If same token is generated, it overwrites previous session (collision)
        login_app.login("guest", "guest")
        # Second login overwrites first due to same token
        assert login_app.SESSIONS["5000"]["username"] == "guest"

        # Only 9000 possible tokens, easy to brute force
        # No token uniqueness checking or collision handling
        assert len(login_app.SESSIONS) == 1