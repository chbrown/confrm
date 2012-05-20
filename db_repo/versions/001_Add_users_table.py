from sqlalchemy import Table, Column, Integer, Unicode, UnicodeText, DateTime, Boolean, MetaData
meta = MetaData()

users = Table(
    'users', meta,
    Column('id', Integer, primary_key=True),
    Column('email', Unicode),
    Column('password', Unicode),
    Column('first_name', Unicode),
    Column('middle_name', Unicode),
    Column('last_name', Unicode),

    Column('classification', Unicode),  # their primary category (student, lecturer)
    Column('institution', Unicode),
    Column('department', Unicode),
    Column('international', Boolean),

    Column('url', Unicode),
    Column('photo', Unicode),
    Column('biography', Unicode),

    Column('tags', Unicode),  # other categories they belong to
    Column('notes', Unicode),
    Column('json', UnicodeText),

    Column('created', DateTime),
    Column('created_by', Integer),
    Column('archived', DateTime),
    Column('archived_by', Integer),
    Column('deleted', DateTime),
    Column('deleted_by', Integer),
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    users.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    users.drop()
