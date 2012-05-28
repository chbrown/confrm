# import re
from datetime import datetime
from pyramid.httpexceptions import HTTPFound
from confrm.handlers import BaseHandler
from confrm.models import DBSession, File, FileGroup, GroupUser, FileUser

class FileHandler(BaseHandler):
    def __route__(self, args):
        self.path = ['files', args[0]]
        getattr(self, args[0])(*args[1:])

    def index(self, *args):
        group_files = DBSession.query(File).\
            filter(File.deleted==None).\
            join(FileGroup, File.id==FileGroup.file_id).\
            join(GroupUser, FileGroup.group_id==GroupUser.group_id).\
            filter(GroupUser.user_id==self.user.id).all()
        user_files = DBSession.query(File).\
            filter(File.deleted==None).\
            join(FileUser, FileUser.user_id==self.user.id).all()
        # filenames = os.listdir(self.localdir)
        self.ctx.group_files = group_files
        self.ctx.user_files = user_files
        # [filename for filename in filenames if not filename.startswith('.')]

    def create(self, *args):
        self.format = 'json'

        upload = self.request.POST['files[]']
        # name = upload.filename
        new_file = File(filename=upload.filename)
        DBSession.add(new_file)
        DBSession.flush()
        file_user = FileUser(user_id=self.user.id, file_id=new_file.id, owner=True)
        DBSession.add(file_user)
        group_id = self.request.POST.get('group_id')
        if group_id:
            file_group = FileGroup(group_id=group_id, file_id=new_file.id, owner=False)
            DBSession.add(file_group)
        DBSession.flush()

        file_size = new_file.read(upload.file)
        print 'file_size', file_size
        # shutil.copyfileobj(f.file, fdst)

        res = dict(
            name=new_file.filename,
            size=file_size,
            url='/files/show/%s' % new_file.id,
            delete_url='/files/delete/%s' % new_file.id,
            delete_type='DELETE'
        )
        self.ctx = [res]

    def delete(self, file_id):
        file_object = DBSession.query(File).get(file_id)
        self.can_modify(file_object)
        file_object.deleted = datetime.now()
        DBSession.flush()

        message = "%s deleted." % file_object.filename
        if self.request.method == 'GET':
            raise HTTPFound(location='/files/index?message=%s' % message)

        self.set_ctx(success=True, message=message)
