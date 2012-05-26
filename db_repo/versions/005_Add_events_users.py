from sqlalchemy import Table, Column, MetaData, ForeignKey, text, \
    Integer, Unicode, DateTime
meta = MetaData()

events_users = Table(
    'events_users', meta,
    Column('id', Integer, primary_key=True),
    Column('event_id', Integer, ForeignKey('events.id')),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id')),
    Column('starts', DateTime),
    Column('ends', DateTime),

    Column('created', DateTime, server_default=text('NOW()')),
    Column('created_by_id', Integer, ForeignKey('users.id')),
    Column('deleted', DateTime),
    Column('deleted_by_id', Integer, ForeignKey('users.id'))
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    Table('events', meta, autoload=True, autoload_with=migrate_engine)
    Table('users', meta, autoload=True, autoload_with=migrate_engine)
    Table('roles', meta, autoload=True, autoload_with=migrate_engine)
    events_users.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    events_users.drop()
