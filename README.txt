# Running

cd ~/work/confrm-dev
pserve --reload src/development.ini

# Migration examples:

    003_Add_role_to_user.py
    # up:
    users = Table('users', meta, autoload=True)
    role_column = Column('role', Unicode(128))
    role_column.create(users)
    # down:
    users = Table('users', meta, autoload=True)
    users.c.role.drop()

    004_Add_fks_to_users_and_events.py
    from sqlalchemy import Table, MetaData
    from migrate.changeset.constraint import ForeignKeyConstraint
    meta = MetaData()

    def fks(table, users_table):
        return [
            ForeignKeyConstraint([table.c.created_by],  [users_table.c.id]),
            ForeignKeyConstraint([table.c.deleted_by],  [users_table.c.id]),
            ForeignKeyConstraint([table.c.archived_by], [users_table.c.id])]

    # up
    users = Table('users', meta, autoload=True)
    events = Table('events', meta, autoload=True)
    for fk in fks(users, users) + fks(events, users):
        fk.create()

    #down
    users = Table('users', meta, autoload=True)
    events = Table('events', meta, autoload=True)
    for fk in fks(users, users) + fks(events, users):
        fk.drop()
