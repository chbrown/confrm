from mixins import mixin_tags_json
from sqlalchemy import Table, Column, MetaData, text, Integer, Unicode, DateTime
meta = MetaData()

# simple enumeration type
organizations = Table(
    'organizations', meta,
    Column('id', Integer, primary_key=True),
    Column('slug', Unicode, nullable=False),
    Column('name', Unicode, nullable=False),

    Column('created', DateTime, server_default=text('NOW()')),
)
mixin_tags_json(organizations)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    organizations.create()

def downgrade(migrate_engine):
    meta.bind = migrate_engine
    organizations.drop()
