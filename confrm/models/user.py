from sqlalchemy.orm import relationship
from confrm.models import DeclarativeBase, DBSession
from confrm.models.tables import users, user_sessions
from confrm.models.group import Group, GroupUser
# from confrm.models.role import Role

class UserSchema(DeclarativeBase):
    __table__ = users
    created_by  = relationship('User', primaryjoin=__table__.c.created_by_id==users.c.id)
    deleted_by  = relationship('User', primaryjoin=__table__.c.deleted_by_id==users.c.id)
    archived_by = relationship('User', primaryjoin=__table__.c.archived_by_id==users.c.id)
    # role =        relationship('Role', primaryjoin=__table__.c.role_id==roles.c.id)

class UserSession(DeclarativeBase):
    __table__ = user_sessions
    user = relationship('User', primaryjoin=__table__.c.user_id==users.c.id)

class User(UserSchema):
    def group_role(self, group_id):
        return DBSession.query(GroupUser).filter(GroupUser.group_id==group_id).filter(GroupUser.user_id==self.id).first()

    def can_edit(self, resource):
        if isinstance(resource, User):
            return self.role in ['superuser', 'admin'] or self == resource
        elif isinstance(resource, Group):
            return self.group_role(resource.id) in ['superuser', 'admin', 'teacher']
        else:
            return False

    @property
    def full_email(self):
        full_name = self.full_name
        if full_name:
            return '"%s" <%s>' % (full_name, self.email)
        return self.email

    @property
    def full_name(self):
        return ' '.join(filter(None, self.first_name, self.last_name))

    def merge(self, other_user):
        for col in self.__table__.columns:
            field = col.name
            other_value = getattr(other_user, field, None)
            if other_value:
                setattr(self, field, other_value)
