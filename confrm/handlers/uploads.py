import os
import re
from pyramid.httpexceptions import HTTPFound
import sqlalchemy.exc
from confrm.handlers import BaseHandler
from confrm.models import DBSession
from confrm.models.role import Role
from confrm.models.user import User
from confrm.lib.table import read_table
import transaction

def parse_request(request):
    if request.content_type == 'application/json':
        return request.json_body
    # application/x-www-form-urlencoded
    return request.POST

def update_attributes(obj, dictionary):
    for key, val in dictionary.items():
        setattr(obj, key, val)

class UploadHandler(BaseHandler):
    """
    1a. The user goes to /uploads/index to upload a file, csv or xls
    1b. They POST their file with jQuery-File-Upload to /uploads/create
    2.  The user goes to /uploads/index to view the uploaded files
    3a. They pick one, going to /uploads/edit?filename=abcdef.xls
    3b. On that page, they can set mappings, functions, cleaners, etc.
    4.  Their settings are saved as an "upload_filter," and they go to /uploads/show?filename=abcdef.xls, to preview the way their data will look like after their filter is applied, resulting in how my app will show it.
    """
    base = 'uploads'

    def __route__(self, request):
        # super(UploadHandler, self).__init__(request)
        # return Response('hi')

        args = request.matchdict['args']
        self.path = [self.base, args[0]]
        getattr(self, args[0])(*args[1:])

    def index(self, *args):
        filenames = os.listdir(self.localdir)
        self.ctx.uploads = [filename for filename in filenames if not filename.startswith('.')]

    def show(self, filename):
        self.ctx.filename = filename
        filepath = '%s/%s' % (self.localdir, filename)
        with open(filepath) as fp:
            rows = read_table(filename, fp)
            flat_row_0 = ' '.join(rows[0])
            if len(re.findall('email|first|last|name', flat_row_0, re.I)) > 0:
                print 'found match'
                self.ctx.headers = rows[0]
                self.ctx.data = rows[1:]
            else:
                self.ctx.data = rows
                headers = []
                for cell in rows[0]:
                    if '@' in cell:
                        headers.append('email')
                    elif ' ' in cell:
                        headers.append('full_name')
                    elif 'first_name' not in headers:
                        headers.append('first_name')
                    elif 'last_name' not in headers:
                        headers.append('last_name')
                    else:
                        headers.append('')
                self.ctx.headers = headers

    def create(self, *args):
        self.format = 'json'

        upload = self.request.params['files[]']
        localpath = '%s/%s' % (self.localdir, upload.filename)
        with open(localpath, 'wb') as fp:
            file_contents = upload.file.read()
            file_size = len(file_contents)
            fp.write(file_contents)

        # shutil.copyfileobj(f.file, fdst)

        resource_url = '/uploads/show/%s' % upload.filename
        res = dict(
            name=upload.filename,
            size=file_size,
            url=resource_url,
            delete_url=resource_url,
            delete_type='DELETE'
        )
        self.ctx = [res]

    def update(self, filename):
        params = parse_request(self.request)

        tag_csv = ','.join(params['tags'])
        role = DBSession.query(Role).filter(Role.name==params['role']).first()
        for user_dict in params['users']:
            try:
                user = User(**user_dict)
                if tag_csv:
                    user.tags = tag_csv
                if role:
                    user.role_id = role.id
                # savepoint = transaction.savepoint()
                DBSession.begin_nested()
                DBSession.add(user)
                DBSession.flush()
                # savepoint = None
                print 'Adding user', user_dict['email']
            except sqlalchemy.exc.IntegrityError, exc:
                DBSession.rollback()
                # transaction.abort()
                print 'Duplicate key error', user_dict['email']
                self.flash(str(exc), success=False)
                # resolve duplicate user
                user = DBSession.query(User).filter(User.email==user_dict['email']).first()
                update_attributes(user, user_dict)
                DBSession.flush()
                print 'Updating user', user_dict['email']
            # except Exception, exc:
                # print 'Other error', exc

    def delete(self, filename):
        filename = filename.replace('..', '')
        os.remove('%s/%s' % (self.localdir, filename))

        self.ctx.message = "%s deleted." % filename
        if self.request.method == 'POST':
            self.ctx.success = True
        else:
            raise HTTPFound(location='/uploads/index?message=%s' % self.ctx.message)

    @property
    def localdir(self):
        dirpath = '%s/files' % self.request.registry.settings['package_directory']
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
        return dirpath
