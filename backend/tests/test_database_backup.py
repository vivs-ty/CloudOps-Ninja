import pytest
import tempfile
import os
import gzip
import sqlite3
from pathlib import Path
from database_backup import DatabaseBackup


class TestDatabaseBackup:
    """Test cases for database backup and restore functionality."""

    def setup_method(self):
        """Create a temporary SQLite database and a backup manager."""
        self.db_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db_file.close()

        self.conn = sqlite3.connect(self.db_file.name)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            "CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL)"
        )
        self.cursor.execute(
            "CREATE TABLE servers (id INTEGER PRIMARY KEY, cloud TEXT UNIQUE NOT NULL, count INTEGER DEFAULT 2, status TEXT DEFAULT 'healthy', cpu INTEGER DEFAULT 20, memory INTEGER DEFAULT 40)"
        )
        self.cursor.execute(
            "CREATE TABLE deployments (id INTEGER PRIMARY KEY, cloud TEXT NOT NULL, version TEXT NOT NULL, timestamp TEXT DEFAULT CURRENT_TIMESTAMP, status TEXT DEFAULT 'success')"
        )
        self.conn.commit()

        self.backup_dir = tempfile.mkdtemp()
        self.backup_manager = DatabaseBackup(self.db_file.name, self.backup_dir)

    def teardown_method(self):
        """Remove the temporary database and backup files."""
        self.conn.close()
        try:
            os.unlink(self.db_file.name)
        except OSError:
            pass

        for file_path in Path(self.backup_dir).glob('*'):
            try:
                file_path.unlink()
            except OSError:
                pass

        try:
            os.rmdir(self.backup_dir)
        except OSError:
            pass

    def test_backup_creation(self):
        self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('testuser', 'hash'))
        self.conn.commit()

        backup_path = self.backup_manager.create_backup('test_backup')

        assert isinstance(backup_path, str)
        assert backup_path.endswith('.db.gz')
        assert Path(backup_path).exists()

    def test_backup_restoration(self):
        self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('user1', 'hash1'))
        self.conn.commit()

        backup_path = self.backup_manager.create_backup('restore_test')
        assert Path(backup_path).exists()

        self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('user2', 'hash2'))
        self.conn.commit()
        self.cursor.execute("SELECT COUNT(*) FROM users")
        assert self.cursor.fetchone()[0] == 2

        self.conn.close()
        result = self.backup_manager.restore_backup(Path(backup_path).name)
        assert result is True

        self.conn = sqlite3.connect(self.db_file.name)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT COUNT(*) FROM users")
        assert self.cursor.fetchone()[0] == 1

    def test_backup_validation(self):
        self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('testuser', 'hash'))
        self.conn.commit()

        backup_path = self.backup_manager.create_backup('validation_test')
        assert Path(backup_path).exists()

        is_valid, message = self.backup_manager.validate_backup(Path(backup_path).name)
        assert is_valid is True
        assert 'valid' in message.lower()

    def test_data_export(self):
        self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('export_user', 'hash'))
        self.cursor.execute(
            "INSERT INTO servers (cloud, count, status, cpu, memory) VALUES (?, ?, ?, ?, ?)",
            ('aws', 1, 'active', 50, 60),
        )
        self.conn.commit()

        data = self.backup_manager.export_data()
        assert isinstance(data, dict)
        assert 'tables' in data
        assert 'users' in data['tables']
        assert 'servers' in data['tables']
        assert data['tables']['users'][0]['username'] == 'export_user'

    def test_data_import(self):
        export_data = {
            'tables': {
                'users': [
                    {'username': 'imported_user', 'password': 'hash'}
                ],
                'servers': [
                    {'cloud': 'gcp', 'count': 2, 'status': 'active', 'cpu': 30, 'memory': 50}
                ]
            }
        }

        result = self.backup_manager.import_data(export_data)
        assert result is True

        self.cursor.execute("SELECT COUNT(*) FROM users")
        assert self.cursor.fetchone()[0] == 1
        self.cursor.execute("SELECT COUNT(*) FROM servers")
        assert self.cursor.fetchone()[0] == 1

    def test_cleanup_old_backups(self):
        for i in range(5):
            self.backup_manager.create_backup(f'cleanup_test_{i}')

        deleted = self.backup_manager.cleanup_old_backups(keep_count=2)
        assert deleted == 3
        assert len(list(Path(self.backup_dir).glob('*.gz'))) == 2

    def test_list_backups(self):
        self.backup_manager.create_backup('list_test_1')
        self.backup_manager.create_backup('list_test_2')

        backups = self.backup_manager.list_backups()
        assert len(backups) == 2
        assert backups[0]['name'].startswith('list_test_')

    def test_backup_with_no_data(self):
        backup_path = self.backup_manager.create_backup('empty_backup')
        assert Path(backup_path).exists()

        is_valid, _ = self.backup_manager.validate_backup(Path(backup_path).name)
        assert is_valid is True

    def test_invalid_backup_path(self):
        is_valid, message = self.backup_manager.validate_backup('non-existent.gz')
        assert is_valid is False
        assert 'does not exist' in message.lower()

        with pytest.raises(FileNotFoundError):
            self.backup_manager.restore_backup('non-existent.gz')

    def test_corrupted_backup_file(self):
        corrupted_path = Path(self.backup_dir) / 'corrupted.gz'
        with gzip.open(corrupted_path, 'wb') as f:
            f.write(b'invalid sqlite data')

        is_valid, _ = self.backup_manager.validate_backup(corrupted_path.name)
        assert is_valid is False

        with pytest.raises(Exception):
            self.backup_manager.restore_backup(corrupted_path.name)

        backup_path = self.backup_manager.create_backup('restore_test')
        assert Path(backup_path).exists()

        self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('user2', 'hash2'))
        self.conn.commit()
        self.cursor.execute("SELECT COUNT(*) FROM users")
        assert self.cursor.fetchone()[0] == 2

        self.conn.close()
        result = self.backup_manager.restore_backup(Path(backup_path).name)
        assert result is True

        self.conn = sqlite3.connect(self.db_file.name)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT COUNT(*) FROM users")
        assert self.cursor.fetchone()[0] == 1

    def test_invalid_backup_path(self):
        is_valid, message = self.backup_manager.validate_backup('non-existent.gz')
        assert is_valid is False
        assert 'does not exist' in message.lower()

        with pytest.raises(FileNotFoundError):
            self.backup_manager.restore_backup('non-existent.gz')

    def test_corrupted_backup_file(self):
        corrupted_path = Path(self.backup_dir) / 'corrupted.gz'
        with gzip.open(corrupted_path, 'wb') as f:
            f.write(b'invalid sqlite data')

        is_valid, _ = self.backup_manager.validate_backup(corrupted_path.name)
        assert is_valid is False

        with pytest.raises(Exception):
            self.backup_manager.restore_backup(corrupted_path.name)