from sqlalchemy import Table, Column, MetaData, ForeignKey, func, \
    Integer, Unicode, UnicodeText, DateTime
meta = MetaData()

events = Table(
    'events', meta,
    Column('id', Integer, primary_key=True),
    Column('name', Unicode),
    Column('tags', Unicode),

    Column('json', UnicodeText),

    Column('created', DateTime, default=func.now()),
    Column('created_by_id', Integer, ForeignKey("users.id")),
    Column('archived', DateTime),
    Column('archived_by_id', Integer, ForeignKey("users.id")),
    Column('deleted', DateTime),
    Column('deleted_by_id', Integer, ForeignKey("users.id")),
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    Table('users', meta, autoload=True, autoload_with=migrate_engine)
    events.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    events.drop()
