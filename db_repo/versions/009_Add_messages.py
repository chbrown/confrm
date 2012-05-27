from mixins import mixin_tags_json, mixin_cad, load
from sqlalchemy import Table, Column, MetaData, ForeignKey, Integer, Unicode
meta = MetaData()

messages = Table(
    'messages', meta,
    Column('id', Integer, primary_key=True),
    Column('subject', Unicode, nullable=False),
    Column('body', Unicode, nullable=False),
    Column('group_id', Integer, ForeignKey('groups.id')),
)
mixin_tags_json(messages)
mixin_cad(messages)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    load(meta, migrate_engine, 'users', 'groups')
    messages.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    messages.drop()
