from confrm.session import DBSession, metadata
from sqlalchemy.ext.declarative import declarative_base

def update(self, kw):
    for k, v in kw.items():
        setattr(self, k, v)

BaseModel = declarative_base(metadata=metadata)
BaseModel.update = update


# class CADMixin(object):
#     __table__ = None
#     created_by  = relationship('User', primaryjoin=__table__.c.created_by_id==users.c.id)
#     archived_by = relationship('User', primaryjoin=__table__.c.archived_by_id==users.c.id)
#     deleted_by  = relationship('User', primaryjoin=__table__.c.deleted_by_id==users.c.id)

from organization import Organization, OrganizationUser
from group import Group, GroupUser
from user import User, UserSession
from .file import File, FileGroup, FileUser
from message import Message
