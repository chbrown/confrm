import os
import re
from pyramid.threadlocal import get_current_registry
from confrm.models import DeclarativeBase, DBSession, GroupUser
from confrm.models.tables import files, files_groups, files_users

class FileGroup(DeclarativeBase):
    __table__ = files_groups

class FileUser(DeclarativeBase):
    __table__ = files_users

class File(DeclarativeBase):
    __table__ = files

    @property
    def directory(self):
        settings = get_current_registry().settings
        dirpath = os.path.join(settings['package_directory'], 'files')
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
        return dirpath

    @property
    def safe_filename(self):
        safe_filename = re.sub(r'/|\\', '', self.filename)
        return re.sub(r'\.+', '.', safe_filename)

    @property
    def filepath(self):
        return '%s/%d-%s' % (self.directory, self.id, self.safe_filename)

    def read(self, fp):
        with open(self.filepath, 'wb') as local_fp:
            file_contents = fp.read()
            file_size = len(file_contents)
            local_fp.write(file_contents)
        return file_size

    def modifiable_by(self, user):
        # try whether the file is directly owned, first
        file_user = DBSession.query(FileUser).\
            filter(FileUser.file_id==self.id).\
            filter(FileUser.user_id==user.id).first()
        if file_user:
            return True
        else:
            # then whether its owned by a group, by proxy
            file_group = DBSession.query(FileGroup).\
                filter(FileGroup.file_id==self.id).\
                join(GroupUser, FileGroup.group_id==GroupUser.group_id).\
                filter(GroupUser.user_id==user.id).first()
            if file_group:
                return True
        return False

    def __json__(self):
        return dict(filename=self.filename, safe_filename=self.safe_filename)
