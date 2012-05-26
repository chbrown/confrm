from sqlalchemy import Table, Column, ForeignKey, MetaData, text, \
    Integer, Unicode, UnicodeText, DateTime, Boolean
meta = MetaData()

users = Table(
    'users', meta,
    Column('id', Integer, primary_key=True),
    Column('email', Unicode, unique=True),
    Column('password', Unicode),
    Column('first_name', Unicode),
    Column('middle_name', Unicode),
    Column('last_name', Unicode),
    Column('other_emails', Unicode),
    Column('role_id', Integer, ForeignKey('roles.id')),

    Column('classification', Unicode),
    Column('institution', Unicode),
    Column('department', Unicode),
    Column('international', Boolean),

    Column('url', Unicode),
    Column('photo', Unicode),
    Column('biography', Unicode),

    Column('tags', Unicode),  # other categories they belong to
    Column('notes', Unicode),
    Column('json', UnicodeText),

    Column('created', DateTime, server_default=text('NOW()')),
    Column('created_by_id', Integer, ForeignKey('users.id')),
    Column('archived', DateTime),
    Column('archived_by_id', Integer, ForeignKey('users.id')),
    Column('deleted', DateTime),
    Column('deleted_by_id', Integer, ForeignKey('users.id'))
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    Table('roles', meta, autoload=True, autoload_with=migrate_engine)
    users.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    users.drop()
