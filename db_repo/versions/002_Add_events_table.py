from sqlalchemy import Table, Column, Integer, Unicode, UnicodeText, DateTime, MetaData
meta = MetaData()

events = Table(
    'events', meta,
    Column('id', Integer, primary_key=True),
    Column('name', Unicode),
    Column('tags', Unicode),

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
    events.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    events.drop()
