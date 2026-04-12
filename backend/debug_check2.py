import tempfile
import os
import gzip
from pathlib import Path
from app import app, db, User
from database_backup import DatabaseBackup

fd = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
fd.close()
path = Path(fd.name).as_posix()
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{path}'
ctx = app.app_context()
ctx.push()

db.create_all()
u = User(username='debuguser', password='hash')
db.session.add(u)
db.session.commit()
print('db path', fd.name)
print('uri', app.config['SQLALCHEMY_DATABASE_URI'])
print('engine url', db.engine.url)
print('db file size', os.path.getsize(fd.name))
print('db header', open(fd.name,'rb').read(16))

tmpdir = tempfile.mkdtemp()
backup_path = DatabaseBackup(fd.name, tmpdir).create_backup('debug_test')
print('backup path', backup_path)
with gzip.open(backup_path, 'rb') as f:
    b = f.read(16)
    print('decompressed header', b)
    print('startswith sqlite', b.startswith(b'SQLite format 3'))
ctx.pop()
