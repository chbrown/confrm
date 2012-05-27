from sqlalchemy.orm import relationship
from confrm.models import DeclarativeBase
from confrm.models.tables import users, groups, groups_users, roles

class Group(DeclarativeBase):
    __table__ = groups
    created_by  = relationship('User', primaryjoin=__table__.c.created_by_id==users.c.id)
    deleted_by  = relationship('User', primaryjoin=__table__.c.deleted_by_id==users.c.id)
    archived_by = relationship('User', primaryjoin=__table__.c.archived_by_id==users.c.id)

class GroupUser(DeclarativeBase):
    __table__ = groups_users
    group = relationship('Group',     primaryjoin=__table__.c.group_id==groups.c.id)
    user = relationship('User',       primaryjoin=__table__.c.user_id==users.c.id)
    role = relationship('Role',       primaryjoin=__table__.c.role_id==roles.c.id)
    created_by = relationship('User', primaryjoin=__table__.c.created_by_id==users.c.id)
    deleted_by = relationship('User', primaryjoin=__table__.c.deleted_by_id==users.c.id)
