# import re
from datetime import datetime
from pyramid.httpexceptions import HTTPFound
from confrm.lib import parse_request
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
    def __route__(self, args):
        self.path = ['files', args[0]]
        getattr(self, args[0])(*args[1:])

    def index(self, *args):
        pass

    def new(self, *args):
        pass

    def data(self, *args):
        group_files = DBSession.query(File).\
            filter(File.deleted==None).\
            join(FileGroup, File.id==FileGroup.file_id).\
            join(GroupUser, FileGroup.group_id==GroupUser.group_id).\
            filter(GroupUser.user_id==self.user.id).all()
        user_files = DBSession.query(File).\
            filter(File.deleted==None).\
            join(FileUser, FileUser.user_id==self.user.id).all()
        # filenames = os.listdir(self.localdir)
        # self.ctx.group_files = group_files
        # self.ctx.user_files = user_files
        self.ctx.data = group_files + user_files
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
        self.set(success=True, message='Added file, %s' % new_file.filename, id=new_file.id)

    def show(self, file_id):
        file_object = DBSession.query(File).get(file_id)
        with open(file_object.filepath, 'r') as local_fp:
            file_contents = local_fp.read(65536)
        self.set(file=file_object, file_contents=file_contents)

    def delete(self, file_id):
        file_object = DBSession.query(File).get(file_id)
        self.can_modify(file_object)
        file_object.deleted = datetime.now()
        DBSession.flush()

        message = "%s deleted." % file_object.filename
        if self.request.method == 'GET':
            raise HTTPFound(location='/files/index?message=%s' % message)

        self.set(success=True, message=message)
