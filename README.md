# To-do

DONE 1. Rename Events to Groups, remove json. Just have role, and maybe tags.
2. Recreate Events, with group_id column. Or maybe have it inherit? Except that I hate polymorphic inheritance in a databse.
3. Create dashboard.
  For superusers, this won't be much.
  For teachers, it would allow uploads and emails.
  For students, it would be basically emails they've been sent and files they have access to.
4. Each action has a list of (view|modify, resource) pairs
4b. If there are any (mod, x) entries, require the request to be a POST, to beat XSS attacks.
5. organization object. Every group has an organization id. There are user_organization attachments.
6. will users have any per-organization preferences?
  Not a big issue, since most deploys will be 1-org.
  But you can stick that stuff on user_organizations many2many's
  What user info is per-org?
7. Store emails as broadcasts, attached to an event.



# Running

cd ~/work/confrm-dev
source bin/activate
pserve --reload src/development.ini

# User set-up

There are three levels:

admin (superusers)
teachers (lecturers/presenters)
students (don't necessarily need to log in, I don't think)

# DB Initialization / updates

createdb confrm_dev
# migrate create db_repo "ConfRM Database Repository"
migrate manage db_repo/manage.py --repository=db_repo --url=postgresql://localhost/confrm_dev
python db_repo/manage.py version_control
python db_repo/manage.py upgrade

# Amazon SES (for sending email) config

Put the following in /etc/boto.cfg

    [Credentials]
    aws_access_key_id=<your_key>
    aws_secret_access_key=<your_secret_key>

Or make them env variables:

    export AWS_ACCESS_KEY_ID=SAKSAUI21AS98213AWE8
    export AWS_SECRET_ACCESS_KEY=AAKSD9aLPOi898LASOWI7naLA8an2NEW7cn9ALHE

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
