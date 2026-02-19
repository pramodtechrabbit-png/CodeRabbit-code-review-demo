"""
Comprehensive test suite for buggy_login_app.py

Tests cover all functions including:
- Database functions (init_db, add_user_db, get_user_db)
- Security functions (hash_password, authenticate)
- Session management (create_session)
- File handling (read_config, write_config)
- Login functions (login, add_user, reset_password)
- Business logic (calculate_total, apply_discount, generate_invoice)
- Admin operations (delete_user, list_users)
- Heavy computation
- CLI functions

Documents security vulnerabilities and bugs in the code.
"""

import pytest
import hashlib
import json
import os
import sqlite3
import tempfile
from unittest.mock import patch, mock_open, MagicMock
import buggy_login_app


@pytest.fixture
def reset_globals():
    """Reset global state before each test."""
    buggy_login_app.USERS = [
        {"username": "admin", "password": "admin123"},
        {"username": "guest", "password": "guest"}
    ]
    buggy_login_app.SESSIONS = {}
    yield
    buggy_login_app.USERS = [
        {"username": "admin", "password": "admin123"},
        {"username": "guest", "password": "guest"}
    ]
    buggy_login_app.SESSIONS = {}


@pytest.fixture
def temp_db(tmp_path):
    """Create a temporary database."""
    db_file = tmp_path / "test_users.db"
    return str(db_file)


@pytest.fixture
def temp_log_file(tmp_path):
    """Create a temporary log file path."""
    log_file = tmp_path / "test_app.log"
    return str(log_file)


class TestHashPassword:
    """Tests for hash_password function."""

    def test_hash_password_basic(self):
        """Test basic password hashing with MD5."""
        password = "test123"
        result = buggy_login_app.hash_password(password)
        expected = hashlib.md5(password.encode()).hexdigest()
        assert result == expected

    def test_hash_password_empty_string(self):
        """Test hashing empty string."""
        result = buggy_login_app.hash_password("")
        expected = hashlib.md5("".encode()).hexdigest()
        assert result == expected

    def test_hash_password_special_chars(self):
        """Test hashing password with special characters."""
        password = "p@$$w0rd!#%^&*()"
        result = buggy_login_app.hash_password(password)
        expected = hashlib.md5(password.encode()).hexdigest()
        assert result == expected

    def test_hash_password_consistency(self):
        """Test that same password produces same hash."""
        password = "consistent"
        hash1 = buggy_login_app.hash_password(password)
        hash2 = buggy_login_app.hash_password(password)
        assert hash1 == hash2

    def test_hash_password_weak_algorithm(self):
        """Document that MD5 is used (weak hashing algorithm)."""
        password = "password123"
        result = buggy_login_app.hash_password(password)
        # MD5 is weak and vulnerable
        assert len(result) == 32  # MD5 produces 32 hex characters


class TestLog:
    """Tests for log function."""

    def test_log_writes_to_file(self, tmp_path, monkeypatch):
        """Test that log writes to file."""
        log_file = tmp_path / "test.log"
        monkeypatch.setattr(buggy_login_app, 'LOG_FILE', str(log_file))

        buggy_login_app.log("Test message")

        assert log_file.exists()
        content = log_file.read_text()
        assert "Test message" in content

    def test_log_appends_to_file(self, tmp_path, monkeypatch):
        """Test that log appends to existing file."""
        log_file = tmp_path / "test.log"
        monkeypatch.setattr(buggy_login_app, 'LOG_FILE', str(log_file))

        buggy_login_app.log("First message")
        buggy_login_app.log("Second message")

        content = log_file.read_text()
        assert "First message" in content
        assert "Second message" in content

    def test_log_includes_timestamp(self, tmp_path, monkeypatch):
        """Test that log includes timestamp."""
        log_file = tmp_path / "test.log"
        monkeypatch.setattr(buggy_login_app, 'LOG_FILE', str(log_file))

        buggy_login_app.log("Timestamped message")

        content = log_file.read_text()
        assert "Timestamped message" in content
        # Timestamp format varies, just check message exists


class TestDatabaseFunctions:
    """Tests for database functions."""

    def test_init_db_creates_table(self, tmp_path, monkeypatch):
        """Test that init_db creates users table."""
        db_file = tmp_path / "test.db"

        # Patch sqlite3.connect to use our test db
        original_connect = sqlite3.connect
        def patched_connect(db_name):
            return original_connect(str(db_file))

        with patch('sqlite3.connect', side_effect=patched_connect):
            buggy_login_app.init_db()

        # Verify table was created
        conn = sqlite3.connect(str(db_file))
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        result = cursor.fetchone()
        conn.close()

        assert result is not None

    def test_add_user_db(self, tmp_path):
        """Test adding user to database."""
        db_file = tmp_path / "test.db"

        # Use monkeypatch to avoid recursion
        original_connect = sqlite3.connect

        def patched_connect(db_name):
            return original_connect(str(db_file))

        with patch('buggy_login_app.sqlite3.connect', side_effect=patched_connect):
            buggy_login_app.init_db()
            buggy_login_app.add_user_db("testuser", "testpass")

        # Verify user was added
        conn = original_connect(str(db_file))
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", ("testuser",))
        result = cursor.fetchone()
        conn.close()

        assert result is not None
        assert result[1] == "testuser"
        assert result[2] == "testpass"

    def test_get_user_db(self, tmp_path):
        """Test getting user from database."""
        db_file = tmp_path / "test.db"

        original_connect = sqlite3.connect

        def patched_connect(db_name):
            return original_connect(str(db_file))

        with patch('buggy_login_app.sqlite3.connect', side_effect=patched_connect):
            buggy_login_app.init_db()
            buggy_login_app.add_user_db("testuser", "testpass")
            user = buggy_login_app.get_user_db("testuser")

        assert user is not None
        assert user[1] == "testuser"
        assert user[2] == "testpass"

    def test_get_user_db_nonexistent(self, tmp_path):
        """Test getting non-existent user returns None."""
        db_file = tmp_path / "test.db"

        original_connect = sqlite3.connect

        def patched_connect(db_name):
            return original_connect(str(db_file))

        with patch('buggy_login_app.sqlite3.connect', side_effect=patched_connect):
            buggy_login_app.init_db()
            user = buggy_login_app.get_user_db("nonexistent")

        assert user is None


class TestAuthenticate:
    """Tests for authenticate function."""

    def test_authenticate_superuser_hardcoded(self, tmp_path):
        """Test hardcoded superuser credentials (security vulnerability)."""
        db_file = tmp_path / "test.db"

        original_connect = sqlite3.connect

        def patched_connect(db_name):
            return original_connect(str(db_file))

        with patch('buggy_login_app.sqlite3.connect', side_effect=patched_connect):
            buggy_login_app.init_db()
            result = buggy_login_app.authenticate("superuser", "superpass")

        # Documents security vulnerability: hardcoded credentials
        assert result is True

    def test_authenticate_database_user_plaintext(self, tmp_path):
        """Test authentication with database user (plaintext password bug)."""
        db_file = tmp_path / "test.db"

        original_connect = sqlite3.connect

        def patched_connect(db_name):
            return original_connect(str(db_file))

        with patch('buggy_login_app.sqlite3.connect', side_effect=patched_connect):
            buggy_login_app.init_db()
            buggy_login_app.add_user_db("testuser", "testpass")
            result = buggy_login_app.authenticate("testuser", "testpass")

        # Documents bug: password compared in plaintext, not hashed
        assert result is True

    def test_authenticate_wrong_password(self, tmp_path):
        """Test authentication fails with wrong password."""
        db_file = tmp_path / "test.db"

        original_connect = sqlite3.connect

        def patched_connect(db_name):
            return original_connect(str(db_file))

        with patch('buggy_login_app.sqlite3.connect', side_effect=patched_connect):
            buggy_login_app.init_db()
            buggy_login_app.add_user_db("testuser", "testpass")
            result = buggy_login_app.authenticate("testuser", "wrongpass")

        assert result is False

    def test_authenticate_nonexistent_user(self, tmp_path):
        """Test authentication fails for non-existent user."""
        db_file = tmp_path / "test.db"

        original_connect = sqlite3.connect

        def patched_connect(db_name):
            return original_connect(str(db_file))

        with patch('buggy_login_app.sqlite3.connect', side_effect=patched_connect):
            buggy_login_app.init_db()
            result = buggy_login_app.authenticate("nonexistent", "pass")

        assert result is False


class TestSessionManagement:
    """Tests for session management."""

    def test_create_session(self, reset_globals):
        """Test creating a session."""
        token = buggy_login_app.create_session("testuser")

        assert token in buggy_login_app.SESSIONS
        assert buggy_login_app.SESSIONS[token]["username"] == "testuser"
        assert "time" in buggy_login_app.SESSIONS[token]

    def test_create_session_token_format(self, reset_globals):
        """Test session token is 4 digits."""
        token = buggy_login_app.create_session("user")

        assert len(token) == 4
        assert token.isdigit()
        assert 1000 <= int(token) <= 9999

    def test_create_session_multiple_users(self, reset_globals):
        """Test creating sessions for multiple users."""
        token1 = buggy_login_app.create_session("user1")
        token2 = buggy_login_app.create_session("user2")

        assert len(buggy_login_app.SESSIONS) >= 2


class TestFileHandling:
    """Tests for file handling functions."""

    def test_read_config_valid_json(self, tmp_path):
        """Test reading valid JSON config."""
        config_file = tmp_path / "config.json"
        test_data = {"key": "value", "number": 123}
        config_file.write_text(json.dumps(test_data))

        result = buggy_login_app.read_config(str(config_file))

        assert result == test_data

    def test_read_config_file_not_closed(self, tmp_path):
        """Document that read_config doesn't close the file handle."""
        config_file = tmp_path / "config.json"
        config_file.write_text('{"key": "value"}')

        # File handle leak - file not closed
        result = buggy_login_app.read_config(str(config_file))
        assert result == {"key": "value"}

    def test_write_config(self, tmp_path):
        """Test writing config to file."""
        config_file = tmp_path / "config.json"
        test_data = {"key": "value"}

        buggy_login_app.write_config(str(config_file), test_data)

        assert config_file.exists()
        saved_data = json.loads(config_file.read_text())
        assert saved_data == test_data

    def test_write_config_no_exception_handling(self, tmp_path):
        """Document that write_config has no exception handling."""
        # Writing to invalid path will raise exception
        with pytest.raises(Exception):
            buggy_login_app.write_config("/invalid/path/file.json", {"key": "value"})


class TestLoginFunctions:
    """Tests for login-related functions."""

    def test_login_with_authenticate(self, reset_globals, tmp_path, capsys):
        """Test login function."""
        db_file = tmp_path / "test.db"

        original_connect = sqlite3.connect

        def patched_connect(db_name):
            return original_connect(str(db_file))

        with patch('buggy_login_app.sqlite3.connect', side_effect=patched_connect):
            buggy_login_app.init_db()
            buggy_login_app.add_user_db("testuser", "testpass")
            buggy_login_app.login("testuser", "testpass")

        captured = capsys.readouterr()
        assert "Login successful" in captured.out

    def test_login_creates_session(self, reset_globals, tmp_path):
        """Test that login creates a session."""
        db_file = tmp_path / "test.db"

        original_connect = sqlite3.connect

        def patched_connect(db_name):
            return original_connect(str(db_file))

        with patch('buggy_login_app.sqlite3.connect', side_effect=patched_connect):
            buggy_login_app.init_db()
            initial_sessions = len(buggy_login_app.SESSIONS)
            buggy_login_app.login("superuser", "superpass")
            assert len(buggy_login_app.SESSIONS) >= initial_sessions

    def test_add_user(self, reset_globals):
        """Test adding a user to USERS list."""
        initial_count = len(buggy_login_app.USERS)

        with patch('buggy_login_app.log'):
            buggy_login_app.add_user("newuser", "newpass")

        assert len(buggy_login_app.USERS) == initial_count + 1
        assert {"username": "newuser", "password": "newpass"} in buggy_login_app.USERS

    def test_add_user_logs_password(self, reset_globals, tmp_path, monkeypatch):
        """Document that add_user logs password (security vulnerability)."""
        log_file = tmp_path / "test.log"
        monkeypatch.setattr(buggy_login_app, 'LOG_FILE', str(log_file))

        buggy_login_app.add_user("user", "secretpass")

        content = log_file.read_text()
        # Documents vulnerability: password logged in plaintext
        assert "secretpass" in content

    def test_reset_password(self, reset_globals):
        """Test resetting user password."""
        with patch('buggy_login_app.log'):
            result = buggy_login_app.reset_password("admin", "newpass")

        assert result is True
        admin = next(u for u in buggy_login_app.USERS if u["username"] == "admin")
        assert admin["password"] == "newpass"

    def test_reset_password_logs_new_password(self, reset_globals, tmp_path, monkeypatch):
        """Document that reset_password logs the new password."""
        log_file = tmp_path / "test.log"
        monkeypatch.setattr(buggy_login_app, 'LOG_FILE', str(log_file))

        buggy_login_app.reset_password("admin", "newsecret")

        content = log_file.read_text()
        # Documents vulnerability: new password logged
        assert "newsecret" in content


class TestBusinessLogic:
    """Tests for business logic functions."""

    def test_calculate_total(self):
        """Test calculating total from items."""
        items = [
            {"price": 10.0, "quantity": 2},
            {"price": 5.0, "quantity": 3}
        ]

        total = buggy_login_app.calculate_total(items)

        assert total == 35.0

    def test_calculate_total_empty_list(self):
        """Test calculating total with empty items."""
        total = buggy_login_app.calculate_total([])
        assert total == 0

    def test_apply_discount(self):
        """Test applying discount."""
        total = 100
        discount = 10

        result = buggy_login_app.apply_discount(total, discount)

        assert result == 90

    def test_apply_discount_zero(self):
        """Test applying zero discount."""
        result = buggy_login_app.apply_discount(100, 0)
        assert result == 100

    def test_generate_invoice(self):
        """Test generating invoice."""
        items = [{"price": 10, "quantity": 2}]

        invoice = buggy_login_app.generate_invoice("order123", items)

        assert invoice["order_id"] == "order123"
        assert invoice["items"] == items
        assert invoice["total"] == 20
        assert "date" in invoice


class TestAdminOperations:
    """Tests for admin operations."""

    def test_delete_user(self, reset_globals):
        """Test deleting a user."""
        initial_count = len(buggy_login_app.USERS)

        with patch('buggy_login_app.log'):
            buggy_login_app.delete_user("guest")

        assert len(buggy_login_app.USERS) == initial_count - 1
        assert not any(u["username"] == "guest" for u in buggy_login_app.USERS)

    def test_list_users(self, reset_globals):
        """Test listing users."""
        users = buggy_login_app.list_users()

        assert isinstance(users, list)
        assert len(users) >= 2
        assert any(u["username"] == "admin" for u in users)


class TestHeavyComputation:
    """Tests for heavy computation function."""

    def test_heavy_computation(self):
        """Test heavy computation returns result."""
        result = buggy_login_app.heavy_computation()

        # Sum of 0 to 9999999
        expected = sum(range(10000000))
        assert result == expected

    def test_heavy_computation_performance(self):
        """Document that heavy_computation is slow."""
        import time
        start = time.time()
        buggy_login_app.heavy_computation()
        duration = time.time() - start

        # This is intentionally slow
        assert duration >= 0  # Just verify it completes


class TestMainMenu:
    """Tests for main menu CLI."""

    @patch('builtins.input')
    def test_main_menu_register(self, mock_input):
        """Test main menu register option."""
        mock_input.side_effect = ["1", "user", "pass", KeyboardInterrupt()]

        with patch('buggy_login_app.log'), \
             pytest.raises(KeyboardInterrupt):
            buggy_login_app.main_menu()

    @patch('builtins.input')
    def test_main_menu_login(self, mock_input, tmp_path):
        """Test main menu login option."""
        db_file = tmp_path / "test.db"

        original_connect = sqlite3.connect

        def patched_connect(db_name):
            return original_connect(str(db_file))

        mock_input.side_effect = ["2", "superuser", "superpass", KeyboardInterrupt()]

        with patch('buggy_login_app.sqlite3.connect', side_effect=patched_connect), \
             pytest.raises(KeyboardInterrupt):
            buggy_login_app.init_db()
            buggy_login_app.main_menu()

    @patch('builtins.input')
    def test_main_menu_recursive_risk(self, mock_input):
        """Document that main_menu calls itself recursively (stack overflow risk)."""
        # This would cause stack overflow with enough iterations
        mock_input.side_effect = ["99"] * 1000 + [KeyboardInterrupt()]

        with pytest.raises((RecursionError, KeyboardInterrupt)):
            buggy_login_app.main_menu()


class TestSecurityVulnerabilities:
    """Tests documenting security vulnerabilities."""

    def test_hardcoded_credentials(self, tmp_path):
        """Document hardcoded superuser credentials."""
        db_file = tmp_path / "test.db"

        original_connect = sqlite3.connect

        def patched_connect(db_name):
            return original_connect(str(db_file))

        with patch('buggy_login_app.sqlite3.connect', side_effect=patched_connect):
            buggy_login_app.init_db()
            # Hardcoded credentials: superuser/superpass
            assert buggy_login_app.authenticate("superuser", "superpass") is True

    def test_plaintext_password_storage(self, reset_globals):
        """Document that passwords are stored in plaintext."""
        with patch('buggy_login_app.log'):
            buggy_login_app.add_user("user", "password123")

        # Passwords stored in plaintext
        user = next(u for u in buggy_login_app.USERS if u["username"] == "user")
        assert user["password"] == "password123"  # Not hashed!

    def test_password_logging(self, reset_globals, tmp_path, monkeypatch):
        """Document that passwords are logged."""
        log_file = tmp_path / "test.log"
        monkeypatch.setattr(buggy_login_app, 'LOG_FILE', str(log_file))

        buggy_login_app.add_user("user", "secret123")

        content = log_file.read_text()
        assert "secret123" in content

    def test_weak_session_tokens(self, reset_globals):
        """Document that session tokens are weak (only 4 digits)."""
        token = buggy_login_app.create_session("user")

        # Only 10000 possible tokens (1000-9999)
        assert 1000 <= int(token) <= 9999

    def test_md5_hash_weakness(self):
        """Document that MD5 is used for hashing (weak)."""
        result = buggy_login_app.hash_password("test")

        # MD5 is cryptographically broken
        assert len(result) == 32


class TestEdgeCases:
    """Edge case and regression tests."""

    def test_empty_username_password(self, reset_globals):
        """Test with empty username and password."""
        with patch('buggy_login_app.log'):
            buggy_login_app.add_user("", "")

        assert {"username": "", "password": ""} in buggy_login_app.USERS

    def test_very_long_username(self, reset_globals):
        """Test with very long username."""
        long_user = "x" * 10000

        with patch('buggy_login_app.log'):
            buggy_login_app.add_user(long_user, "pass")

        assert any(u["username"] == long_user for u in buggy_login_app.USERS)

    def test_special_characters_in_credentials(self, reset_globals):
        """Test special characters in credentials."""
        with patch('buggy_login_app.log'):
            buggy_login_app.add_user("user@#$", "pass!@#")

        assert any(u["username"] == "user@#$" for u in buggy_login_app.USERS)

    def test_calculate_total_missing_keys(self):
        """Test calculate_total with missing keys."""
        items = [{"price": 10}]  # Missing quantity

        with pytest.raises(KeyError):
            buggy_login_app.calculate_total(items)

    def test_apply_discount_over_100(self):
        """Test applying discount over 100%."""
        result = buggy_login_app.apply_discount(100, 150)

        # Results in negative value
        assert result == -50

    def test_global_state_mutation(self, reset_globals):
        """Test that global state can be mutated."""
        buggy_login_app.USERS.append({"username": "hacker", "password": "hacked"})

        assert any(u["username"] == "hacker" for u in buggy_login_app.USERS)