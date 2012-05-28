import sqlalchemy.exc
from confrm.lib import parse_request
from confrm.lib.table import read_table, guess_headers
from confrm.handlers import BaseHandler
from confrm.models import DBSession, User, File, Role, Group

class UserHandler(BaseHandler):
    """
    For uploads:
    1a. The user goes to /uploads/index to upload a file, csv or xls
    1b. They POST their file with jQuery-File-Upload to /uploads/create
    2.  The user goes to /uploads/index to view the uploaded files
    3a. They pick one, going to /uploads/edit?filename=abcdef.xls
    3b. On that page, they can set mappings, functions, cleaners, etc.
    4.  Their settings are saved as an "upload_filter," and they go to /uploads/show?filename=abcdef.xls, to preview the way their data will look like after their filter is applied, resulting in how my app will show it.
    """
    base = 'users'

    def index(self):
        users = DBSession.query(User).all()
        self.ctx.users = users

    def new_from_file(self, file_id):
        self.can('')
        # file_id = self.request.GET['file_id']
        new_file = DBSession.query(File).get(file_id)
        with open(new_file.filepath) as fp:
            rows = read_table(new_file.filename, fp)
            self.ctx.headers, self.ctx.data = guess_headers(rows)

    def create(self):
        params = parse_request(self.request)

        tag_csv = ','.join(params['tags'])
        role = DBSession.query(Role).filter(Role.name==params['role']).first()
        group = DBSession.query(Group).filter(Group.id==params['group_id']).first()
        for user_dict in params['users']:
            new_user = User(**user_dict)
            if tag_csv:
                new_user.tags = tag_csv
            if role:
                new_user.role_id = role.id
            if group:
                new_user.group_id = role.id
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
        assert self.can_modify(user)

        params = parse_request(self.request)
        print params.items()
        for key, value in params.items():
            setattr(user, key, value)

        DBSession.add(user)
        DBSession.flush()

        self.ctx.success = True
        self.ctx.message = 'Updated user.'
