import sqlalchemy.exc
from confrm.lib import parse_request
from confrm.handlers import AuthenticatedHandler
from confrm.models import DBSession, User, Group


class UserHandler(AuthenticatedHandler):
    """
    For uploads:
    1a. The user goes to /uploads/index to upload a file, csv or xls
    1b. They POST their file with jQuery-File-Upload to /uploads/create
    2.  The user goes to /uploads/index to view the uploaded files
    3a. They pick one, going to /uploads/edit?filename=abcdef.xls
    3b. On that page, they can set mappings, functions, cleaners, etc.
    4.  Their settings are saved as an "upload_filter," and they go to /uploads/show?filename=abcdef.xls, to preview the way their data will look like after their filter is applied, resulting in how my app will show it.
    """
    def __route__(self, args):
        self.path = ['users', args[0]]
        getattr(self, args[0])(*args[1:])

    def index(self):
        users = DBSession.query(User).all()
        self.ctx.users = users

    def create(self):
        params = parse_request(self.request)

        tag_csv = ','.join(params['tags'])
        group = DBSession.query(Group).filter(Group.id.in_(params['groups'])).first()
        for user_dict in params['users']:
            new_user = User(**user_dict)
            if tag_csv:
                new_user.tags = tag_csv
            if group:
                new_user.group_id = group.id
            try:
                DBSession.begin_nested()
                DBSession.add(new_user)
                DBSession.flush()
                # print 'Adding user', user_dict['email']
            except sqlalchemy.exc.IntegrityError, exc:
                DBSession.rollback()
                self.flash(str(exc), success=False)
                user = DBSession.query(User).filter(User.email==user_dict['email']).first()
                user.merge(new_user)
                DBSession.flush()

    def edit(self, user_id):
        self.ctx.user = DBSession.query(User).get(user_id)
        # print self.ctx.user_object

    def update(self, user_id):
        user = DBSession.query(User).get(user_id)
        self.can_modify(user)

        params = parse_request(self.request)
        print params.items()
        for key, value in params.items():
            setattr(user, key, value)

        DBSession.add(user)
        DBSession.flush()

        self.ctx.success = True
        self.ctx.message = 'Updated user.'
