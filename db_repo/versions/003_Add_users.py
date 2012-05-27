from mixins import mixin_tags_json, mixin_cad, load
from sqlalchemy import Table, Column, MetaData, Integer, Unicode, Boolean
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

    Column('classification', Unicode),
    Column('institution', Unicode),
    Column('department', Unicode),
    Column('international', Boolean),
    Column('notes', Unicode),

    Column('url', Unicode),
    Column('photo', Unicode),
    Column('biography', Unicode),
)
mixin_tags_json(users)
mixin_cad(users)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    load(meta, migrate_engine, 'roles', 'users')
    users.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    users.drop()
