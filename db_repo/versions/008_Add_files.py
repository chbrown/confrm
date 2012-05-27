from mixins import mixin_tags_json, mixin_cad, load
from sqlalchemy import Table, Column, MetaData, Integer, Unicode
meta = MetaData()

files = Table(
    'files', meta,
    Column('id', Integer, primary_key=True),
    Column('filename', Unicode, nullable=False),
    Column('filepath', Unicode, nullable=False),
)
mixin_tags_json(files)
mixin_cad(files)

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    load(meta, migrate_engine, 'users')
    files.create()

def downgrade(migrate_engine):
    meta.bind = migrate_engine
    files.drop()
