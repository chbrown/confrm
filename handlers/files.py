import re
from pyramid.response import FileResponse
from datetime import datetime
from pyramid.httpexceptions import HTTPFound
from confrm.lib import parse_request
from confrm.lib.table import read_table, guess_users
from confrm.handlers import AuthenticatedHandler
from confrm.models import DBSession, File, FileGroup, GroupUser, FileUser


def add_user_file(user, filename):
    new_file = File(filename=filename)
    DBSession.add(new_file)
    DBSession.flush()
    file_user = FileUser(user_id=user.id, file_id=new_file.id, owner=True)
    DBSession.add(file_user)
    DBSession.flush()
    return new_file


class FileHandler(AuthenticatedHandler):
    path = ('files',)

    def index(self, *args):
        group_files = DBSession.query(File).\
            filter(File.deleted==None).\
            join(FileGroup, File.id==FileGroup.file_id).\
            join(GroupUser, FileGroup.group_id==GroupUser.group_id).\
            filter(GroupUser.user_id==self.user.id).all()
        user_files = DBSession.query(File).\
            filter(File.deleted==None).\
            join(FileUser, FileUser.user_id==self.user.id).all()
        self.ctx.files = group_files + user_files

    def new(self, *args):
        pass

    # def data(self, *args):
        # filenames = os.listdir(self.localdir)
        # self.ctx.group_files = group_files
        # self.ctx.user_files = user_files
        # [filename for filename in filenames if not filename.startswith('.')]

    def create(self, *args):
        params = parse_request(self.request)
        filename = params.get('filename')
        if not filename:
            now = datetime.today()
            filename = now.strftime('NA-%Y-%m-%dT%H-%M-%s.txt')
        new_file = add_user_file(self.user, filename)
        new_file.read(params['contents'])

        self.set(success=True, message='Added file, %s' % filename)

    def upload(self, *args):
        """
        Upload spreadsheet:
          1. Get column mapping with custom functions
          2. Save mapping & functions
          3. Show preview
          4. Resolve duplicates
            Possibly interactively?
        """
        upload = self.request.POST['files[]']
        new_file = add_user_file(self.user, upload.filename)
        # group_id = self.request.POST.get('group_id')
        # if group_id:
        #     file_group = FileGroup(group_id=group_id,
            # file_id=new_file.id, owner=False)
        #     DBSession.add(file_group)
        # DBSession.flush()
        new_file.read(upload.file)
        self.set(success=True, message='Added file, %s' % new_file.filename, file=new_file)

    def as_users(self, file_id):
        file_object = DBSession.query(File).get(file_id)
        with open(file_object.filepath, 'r') as fp:
            rows = read_table(file_object.filename, fp)
            self.ctx.users = guess_users(rows)

    def show(self, file_id):
        file_object = DBSession.query(File).get(file_id)
        self.set(**file_object.__json__())
        if re.search('(^[^.]|txt|csv|tab|tsv)$', file_object.filepath, re.I):
            try:
                self.ctx.contents = open(file_object.filepath).read(65535)
            except:
                self.ctx.message = 'File failed'
        elif re.search('jpe?g|png|gif', file_object.filepath, re.I):
            self.ctx.img = '/files/%d/read' % file_object.id
        self.ctx.download = '/files/%d/download' % file_object.id

    def read(self, file_id):
        # this is a publically accessible action!
        self.file_object = DBSession.query(File).get(file_id)
        self.response = FileResponse(self.file_object.filepath)

    def download(self, file_id):
        self.read(file_id)
        self.response.content_disposition = 'attachment; filename="%s"' % self.file_object.filename

    def update(self, file_id):
        file_object = DBSession.query(File).get(file_id)
        file_object.update(self.request.json_body)
        if 'contents' in self.request.json_body:
            file_object.read(self.request.json_body['contents'])
        DBSession.add(file_object)
        # DBSession.flush()

        self.set(success=True, message='File updated.')

    def delete(self, file_id):
        file_object = DBSession.query(File).get(file_id)
        self.can_modify(file_object)
        file_object.deleted = datetime.now()
        DBSession.flush()

        message = "%s deleted." % file_object.filename
        if self.request.method == 'GET':
            raise HTTPFound(location='/files/index?message=%s' % message)

        self.set(success=True, message=message)
