from sqlalchemy import Table, Column, MetaData, ForeignKey, text, \
    Integer, DateTime
meta = MetaData()

groups_users = Table(
    'groups_users', meta,
    Column('id', Integer, primary_key=True),
    Column('group_id', Integer, ForeignKey('groups.id'), nullable=False),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('role_id', Integer, ForeignKey('roles.id')),

    Column('created', DateTime, server_default=text('NOW()')),
    Column('created_by_id', Integer, ForeignKey('users.id')),
    Column('deleted', DateTime),
    Column('deleted_by_id', Integer, ForeignKey('users.id'))
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    Table('groups', meta, autoload=True, autoload_with=migrate_engine)
    Table('users', meta, autoload=True, autoload_with=migrate_engine)
    Table('roles', meta, autoload=True, autoload_with=migrate_engine)
    groups_users.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    groups_users.drop()
