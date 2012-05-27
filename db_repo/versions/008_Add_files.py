from sqlalchemy import Table, Column, MetaData, ForeignKey, text, \
    Integer, Unicode, UnicodeText, DateTime
meta = MetaData()

files = Table(
    'files', meta,
    Column('id', Integer, primary_key=True),
    Column('filename', Unicode, nullable=False),
    Column('filepath', Unicode, nullable=False),
    Column('group_id', Integer, ForeignKey('groups.id')),

    Column('tags', Unicode),
    Column('json', UnicodeText),

    Column('created', DateTime, server_default=text('NOW()')),
    Column('created_by_id', Integer, ForeignKey('users.id')),
    Column('archived', DateTime),
    Column('archived_by_id', Integer, ForeignKey('users.id')),
    Column('deleted', DateTime),
    Column('deleted_by_id', Integer, ForeignKey('users.id')),
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    Table('users', meta, autoload=True, autoload_with=migrate_engine)
    Table('groups', meta, autoload=True, autoload_with=migrate_engine)
    files.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    files.drop()
