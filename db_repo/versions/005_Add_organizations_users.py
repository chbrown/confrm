from sqlalchemy import Table, Column, MetaData, ForeignKey, text, \
    Integer, Unicode, UnicodeText, DateTime
meta = MetaData()

# simple enumeration type
organizations_users = Table(
    'organizations_users', meta,
    Column('id', Integer, primary_key=True),
    Column('organization_id', Integer, ForeignKey('organizations.id'), nullable=False),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('role_id', Integer, ForeignKey('roles.id')),

    Column('tags', Unicode),
    Column('json', UnicodeText),

    Column('created', DateTime, server_default=text('NOW()')),
    Column('created_by_id', Integer, ForeignKey('users.id')),
    Column('archived', DateTime),
    Column('created_by_id', Integer, ForeignKey('users.id')),
    Column('deleted', DateTime),
    Column('deleted_by_id', Integer, ForeignKey('users.id'))
)

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    organizations_users.create()

def downgrade(migrate_engine):
    meta.bind = migrate_engine
    organizations_users.drop()
