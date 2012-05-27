from sqlalchemy import Table, Column, MetaData, text, \
    Integer, Unicode, UnicodeText, DateTime
meta = MetaData()

# simple enumeration type
organizations = Table(
    'organizations', meta,
    Column('id', Integer, primary_key=True),
    Column('slug', Unicode, nullable=False),
    Column('name', Unicode, nullable=False),

    Column('tags', Unicode),
    Column('json', UnicodeText),

    Column('created', DateTime, server_default=text('NOW()')),
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    organizations.create()

    bootstrap_insert = organizations.insert().values(slug=u'nasslli2012', name=u'NASSLLI 2012')
    migrate_engine.execute(bootstrap_insert)


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    organizations.drop()