from mixins import mixin_cad, load
from sqlalchemy import Table, Column, MetaData, ForeignKey, Integer, Boolean, text
meta = MetaData()

groups_users = Table(
    'groups_users', meta,
    Column('id', Integer, primary_key=True),
    Column('group_id', Integer, ForeignKey('groups.id'), nullable=False),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('owner', Boolean, server_default=text('FALSE'), nullable=False),
)
mixin_cad(groups_users)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    load(meta, migrate_engine, 'users', 'groups')
    groups_users.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    groups_users.drop()
