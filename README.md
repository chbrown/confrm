# ConfRM

ConfRM, which stands for Conference Resource Management, intends to be a way to annotate and manage groups of users. Primary functionality is (/will be):

1. Uploading and importing from several different kinds of spreadsheet (XLS, XLSX, csv, tab), with duplicate handling.
2. Sending emails to groups of students, by tag or group.
3. Uploading files for students to see.

It's intended to be a sort of mini-BlackBoard. Except not violating every convention of web UX.

## Running for Development

	j confrm-dev
	source bin/activate
	cd src/
	python setup.py develop
	pserve --reload development.ini

## DB Initialization / updates

    # dropdb confrm_dev
	createdb confrm_dev
	# migrate create db_repo "ConfRM Database Repository"
	# migrate manage db_repo/manage.py --repository=db_repo --url=postgresql://localhost/confrm_dev
	python db_repo/manage.py version_control
	python db_repo/manage.py upgrade

  	# Get started with a root user, at the CLI:
  	python confrm/scripts/add.py development.ini --email audiere@gmail.com --password needle --slug nasslli2012 --name "NASSLLI 2012"
  
## Amazon SES Config

The app uses Amazon (AWS) Simple Email Service to send email, and `boto` as the API driver. SES pricing, $0.10 per thousand emails, isn't bad, I'd say---because `postfix` is a pain to configure.

Put the following in /etc/boto.cfg

    [Credentials]
    aws_access_key_id=SAKSAUI21AS98213AWE8
    aws_secret_access_key=AAKSD9aLPOi898LASOWI7naLA8an2NEW7cn9ALHE

Or make them env variables:

    export AWS_ACCESS_KEY_ID=SAKSAUI21AS98213AWE8
    export AWS_SECRET_ACCESS_KEY=AAKSD9aLPOi898LASOWI7naLA8an2NEW7cn9ALHE

## Migration examples:

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

# To-do:

1. Create dashboard page:
	1. For superusers, this won't be much. They can do everything, so they don't have anything special to do.
	2. For teachers, it would allow uploads and emails.
	3. For students, it would be basically emails they've been sent and files they have access to.
2. Elegant handling of resources and permissions.
	1. Each action should be decorated with a list of (view|modify, resource) pairs, or run some `assert_permission(self.user, 'modify', resource)` method in the action.
	2. Every `assert_permission(self.user, 'modify', x)` entry should raise an exception if the method is not POST or PUT, to beat XSS attacks.
6. Allow users to have some per-organization preferences, versus global info.
This is not a big issue, since most deploys will be 1-organization. But you can stick that stuff on the organizations_users many2many relationship. (Question: What user info _is_ per-organization?)
7. Outgoing emails should always be recorded ("broadcasts"?), attached to an group.
