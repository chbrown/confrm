from sqlalchemy import MetaData
meta = MetaData()

def upgrade(migrate_engine):
    meta.bind = migrate_engine

def downgrade(migrate_engine):
    meta.bind = migrate_engine
