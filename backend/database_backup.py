#!/usr/bin/env python3
"""
Database Backup and Restore Utilities
Provides functionality to backup and restore SQLite database
"""

import os
import shutil
import sqlite3
import gzip
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from flask import current_app
from logger import get_logger

logger = get_logger(__name__)

class DatabaseBackup:
    """Handles database backup and restore operations"""

    def __init__(self, db_path: str = None, backup_dir: str = None):
        """
        Initialize database backup utility

        Args:
            db_path: Path to SQLite database file
            backup_dir: Directory to store backups
        """
        self.db_path = db_path or current_app.config.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///app.db')
        if self.db_path.startswith('sqlite:///'):
            self.db_path = self.db_path.replace('sqlite:///', '')

        self.backup_dir = Path(backup_dir or 'backups')
        self.backup_dir.mkdir(exist_ok=True)

        logger.info(f"DatabaseBackup initialized: db_path={self.db_path}, backup_dir={self.backup_dir}")

    def create_backup(self, name: str = None, compress: bool = True) -> str:
        """
        Create a database backup

        Args:
            name: Custom backup name (optional)
            compress: Whether to compress the backup

        Returns:
            Path to the created backup file
        """
        if name is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            name = f"backup_{timestamp}"

        backup_name = f"{name}.db"
        if compress:
            backup_name += '.gz'

        backup_path = self.backup_dir / backup_name

        try:
            # Create backup by copying the database file
            if compress:
                with gzip.open(backup_path, 'wb') as f_out:
                    with open(self.db_path, 'rb') as f_in:
                        shutil.copyfileobj(f_in, f_out)
            else:
                shutil.copy2(self.db_path, backup_path)

            logger.info(f"Database backup created: {backup_path}")
            return str(backup_path)

        except Exception as e:
            logger.error(f"Failed to create database backup: {e}")
            raise

    def list_backups(self) -> List[Dict]:
        """
        List all available backups

        Returns:
            List of backup information dictionaries
        """
        backups = []
        for file_path in self.backup_dir.glob('*.db*'):
            stat = file_path.stat()
            backups.append({
                'name': file_path.name,
                'path': str(file_path),
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'compressed': file_path.suffix == '.gz'
            })

        # Sort by creation time (newest first)
        backups.sort(key=lambda x: x['created'], reverse=True)
        return backups

    def restore_backup(self, backup_name: str, create_backup_first: bool = True) -> bool:
        """
        Restore database from backup

        Args:
            backup_name: Name of the backup file to restore
            create_backup_first: Whether to create a backup before restoring

        Returns:
            True if successful
        """
        backup_path = self.backup_dir / backup_name

        if not backup_path.exists():
            raise FileNotFoundError(f"Backup file not found: {backup_path}")

        is_valid, validation_message = self.validate_backup(backup_name)
        if not is_valid:
            raise ValueError(f"Backup validation failed before restore: {validation_message}")

        try:
            # Create a pre-restore backup if requested
            if create_backup_first:
                pre_restore_backup = self.create_backup(f"pre_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
                logger.info(f"Pre-restore backup created: {pre_restore_backup}")

            # Restore the database
            if backup_name.endswith('.gz'):
                with gzip.open(backup_path, 'rb') as f_in:
                    with open(self.db_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
            else:
                shutil.copy2(backup_path, self.db_path)

            logger.info(f"Database restored from backup: {backup_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to restore database from backup: {e}")
            raise

    def export_data(self, tables: List[str] = None) -> Dict:
        """
        Export database data as JSON

        Args:
            tables: List of table names to export (all if None)

        Returns:
            Dictionary containing table data
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Get all tables if not specified
            if tables is None:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
                tables = [row[0] for row in cursor.fetchall()]

            export_data = {
                'export_time': datetime.now().isoformat(),
                'database': self.db_path,
                'tables': {}
            }

            for table in tables:
                cursor.execute(f"SELECT * FROM {table}")
                rows = cursor.fetchall()

                # Convert rows to dictionaries
                table_data = []
                for row in rows:
                    table_data.append(dict(row))

                export_data['tables'][table] = table_data
                logger.info(f"Exported {len(table_data)} rows from table {table}")

            conn.close()
            return export_data

        except Exception as e:
            logger.error(f"Failed to export database data: {e}")
            raise

    def import_data(self, import_data: Dict, mode: str = 'replace') -> bool:
        """
        Import database data from JSON export

        Args:
            import_data: Data dictionary from export_data()
            mode: Import mode ('replace' or 'append')

        Returns:
            True if successful
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            for table_name, rows in import_data.get('tables', {}).items():
                if mode == 'replace':
                    # Clear existing data
                    cursor.execute(f"DELETE FROM {table_name}")

                # Insert new data
                if rows:
                    # Get column names from first row
                    columns = list(rows[0].keys())
                    placeholders = ','.join(['?' for _ in columns])
                    column_names = ','.join(columns)

                    for row in rows:
                        values = [row[col] for col in columns]
                        cursor.execute(f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})", values)

                logger.info(f"Imported {len(rows)} rows into table {table_name}")

            conn.commit()
            conn.close()

            logger.info("Database data import completed")
            return True

        except Exception as e:
            logger.error(f"Failed to import database data: {e}")
            raise

    def get_backup_info(self, backup_name: str) -> Optional[Dict]:
        """
        Get information about a specific backup

        Args:
            backup_name: Name of the backup file

        Returns:
            Backup information dictionary or None if not found
        """
        backup_path = self.backup_dir / backup_name
        if not backup_path.exists():
            return None

        stat = backup_path.stat()
        return {
            'name': backup_name,
            'path': str(backup_path),
            'size': stat.st_size,
            'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
            'compressed': backup_name.endswith('.gz')
        }

    def cleanup_old_backups(self, keep_count: int = 10) -> int:
        """
        Clean up old backups, keeping only the most recent ones

        Args:
            keep_count: Number of recent backups to keep

        Returns:
            Number of backups deleted
        """
        backups = self.list_backups()
        if len(backups) <= keep_count:
            return 0

        # Sort by creation time (oldest first)
        backups_to_delete = backups[keep_count:]

        deleted_count = 0
        for backup in backups_to_delete:
            backup_path = Path(backup['path'])
            try:
                backup_path.unlink()
                logger.info(f"Deleted old backup: {backup_path}")
                deleted_count += 1
            except Exception as e:
                logger.error(f"Failed to delete backup {backup_path}: {e}")

        return deleted_count

    def validate_backup(self, backup_name: str) -> Tuple[bool, str]:
        """
        Validate that a backup file is readable and contains valid data

        Args:
            backup_name: Name of the backup file

        Returns:
            Tuple of (is_valid, message)
        """
        backup_path = self.backup_dir / backup_name

        if not backup_path.exists():
            return False, f"Backup file does not exist: {backup_path}"

        try:
            # Try to open and read the backup
            if backup_name.endswith('.gz'):
                with gzip.open(backup_path, 'rb') as f:
                    header = f.read(16)
            else:
                with open(backup_path, 'rb') as f:
                    header = f.read(16)

            if backup_name.endswith('.gz'):
                with gzip.open(backup_path, 'rb') as f:
                    header = f.read(16)
            else:
                with open(backup_path, 'rb') as f:
                    header = f.read(16)

            if not header.startswith(b'SQLite format 3'):
                return False, "File is not a valid SQLite database"

            return True, "Backup file is valid"

        except gzip.BadGzipFile as e:
            return False, f"Backup validation failed: invalid gzip file ({e})"
        except Exception as e:
            return False, f"Backup validation failed: {e}"