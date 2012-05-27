from sqlalchemy import Table, Column, MetaData, text, \
    Integer, Unicode, DateTime
meta = MetaData()

# simple enumeration type
roles = Table(
    'roles', meta,
    Column('id', Integer, primary_key=True),
    Column('level', Integer, nullable=False),
    Column('name', Unicode, nullable=False),
    Column('created', DateTime, server_default=text('NOW()')),
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    roles.create()

    bootstrap_roles = [
        dict(name=u'superuser', level=0),
        dict(name=u'admin', level=1),
        dict(name=u'teacher', level=10),
        dict(name=u'assistant', level=11),
        dict(name=u'student', level=12)
    ]

    for role in bootstrap_roles:
        migrate_engine.execute(roles.insert().values(**role))


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    roles.drop()
