from sqlalchemy import Table, Column, MetaData, text, \
    Integer, Unicode, ForeignKey, DateTime
meta = MetaData()

user_sessions = Table(
    'user_sessions', meta,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('ticket', Unicode),
    Column('ip', Unicode),
    Column('user_agent', Unicode),

    Column('created', DateTime, server_default=text('NOW()')),
    Column('deleted', DateTime),
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    Table('users', meta, autoload=True, autoload_with=migrate_engine)
    user_sessions.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    user_sessions.drop()
