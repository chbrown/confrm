from confrm.models import DeclarativeBase
from confrm.models.tables import files, files_groups, files_users

class File(DeclarativeBase):
    __table__ = files

class FileGroup(DeclarativeBase):
    __table__ = files_groups

class FileUser(DeclarativeBase):
    __table__ = files_users
