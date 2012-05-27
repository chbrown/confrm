from mixins import mixin_tags_json, mixin_cad, load
from sqlalchemy import Table, Column, MetaData, Integer, Unicode
meta = MetaData()

groups = Table(
    'groups', meta,
    Column('id', Integer, primary_key=True),
    Column('name', Unicode, nullable=False),
)
mixin_tags_json(groups)
mixin_cad(groups)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    load(meta, migrate_engine, 'users')
    groups.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    groups.drop()
