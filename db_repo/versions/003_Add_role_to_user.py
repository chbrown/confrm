from sqlalchemy import Table, Column, Unicode, MetaData
meta = MetaData()


def upgrade(migrate_engine):
    meta.bind = migrate_engine

    users = Table('users', meta, autoload=True)
    role_column = Column('role', Unicode(128))
    role_column.create(users)


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    users = Table('users', meta, autoload=True)
    users.c.role.drop()
