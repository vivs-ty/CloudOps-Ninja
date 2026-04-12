import tempfile
import os
import gzip
from app import app, db, User
from database_backup import DatabaseBackup

fd = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
fd.close()
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{fd.name}'
ctx = app.app_context()
ctx.push()

db.create_all()
user = User(username='debuguser', password='hash')
db.session.add(user)
db.session.commit()
print('db file size', os.path.getsize(fd.name))
print('db header', open(fd.name, 'rb').read(16))

tmpdir = tempfile.mkdtemp()
backup = DatabaseBackup(fd.name, tmpdir).create_backup('debug_test')
print('backup', backup)
with gzip.open(backup, 'rb') as f:
    b = f.read(16)
    print('decompressed header', b)
    print('sqlite?', b.startswith(b'SQLite format 3'))

ctx.pop()
