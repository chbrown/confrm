from mixins import mixin_tags_json, mixin_cad, load
from sqlalchemy import Table, Column, MetaData, ForeignKey, Integer, Boolean, text
meta = MetaData()

# simple enumeration type
organizations_users = Table(
    'organizations_users', meta,
    Column('id', Integer, primary_key=True),
    Column('organization_id', Integer, ForeignKey('organizations.id'), nullable=False),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('owner', Boolean, server_default=text('FALSE'), nullable=False),
)
mixin_tags_json(organizations_users)
mixin_cad(organizations_users)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    load(meta, migrate_engine, 'organizations', 'users')
    organizations_users.create()

def downgrade(migrate_engine):
    meta.bind = migrate_engine
    organizations_users.drop()
