import tempfile
import os

# Create a temporary database
db_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
db_file.close()

# Import after setting up the database file
from app import app, db, User, Server, Deployment

# Create a new db object for this test
from flask_sqlalchemy import SQLAlchemy
test_db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_file.name}'
print(f"Database URI set to: {app.config['SQLALCHEMY_DATABASE_URI']}")
print(f"Database file exists: {os.path.exists(db_file.name)}")

ctx = app.app_context()
ctx.push()
test_db.create_all()

print(f"Database file size after create_all: {os.path.getsize(db_file.name) if os.path.exists(db_file.name) else 0}")

# Create some data
user = User(username='test', password='hash')
test_db.session.add(user)
test_db.session.commit()

print(f"Database file size after adding data: {os.path.getsize(db_file.name) if os.path.exists(db_file.name) else 0}")

# Create some data
user = User(username='test', password='hash')
db.session.add(user)
db.session.commit()

# Check what tables exist
import sqlite3
conn = sqlite3.connect(db_file.name)
cursor = conn.cursor()
cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name NOT LIKE "sqlite_%"')
tables = cursor.fetchall()
print('Tables found:', tables)

# Check export_data
from database_backup import DatabaseBackup
backup_mgr = DatabaseBackup(db_file.name, '/tmp')
export_data = backup_mgr.export_data()
print('Export data tables:', list(export_data['tables'].keys()))

conn.close()
os.unlink(db_file.name)
ctx.pop()