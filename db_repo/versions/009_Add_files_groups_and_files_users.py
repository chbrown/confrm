from mixins import load
from sqlalchemy import Table, Column, MetaData, Integer, ForeignKey, Boolean, text
meta = MetaData()

files_groups = Table(
    'files_groups', meta,
    Column('id', Integer, primary_key=True),
    Column('file_id', Integer, ForeignKey('files.id'), nullable=False),
    Column('group_id', Integer, ForeignKey('groups.id'), nullable=False),
    Column('owner', Boolean, server_default=text('FALSE'), nullable=False),
)

files_users = Table(
    'files_users', meta,
    Column('id', Integer, primary_key=True),
    Column('file_id', Integer, ForeignKey('files.id'), nullable=False),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('owner', Boolean, server_default=text('TRUE'), nullable=False),
)

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    load(meta, migrate_engine, 'files', 'users', 'groups')
    files_groups.create()
    files_users.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    files_groups.drop()
    files_users.drop()
