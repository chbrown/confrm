from sqlalchemy.orm import relationship
from confrm.models import DeclarativeBase
from confrm.models.tables import users, user_sessions, groups_users
# from confrm.models.group import GroupUser

class UserSchema(DeclarativeBase):
    __table__ = users
    created_by  = relationship('User', primaryjoin=__table__.c.created_by_id==users.c.id)
    deleted_by  = relationship('User', primaryjoin=__table__.c.deleted_by_id==users.c.id)
    archived_by = relationship('User', primaryjoin=__table__.c.archived_by_id==users.c.id)

    groups = relationship('Group', secondary=groups_users, backref="users")

class UserSession(DeclarativeBase):
    __table__ = user_sessions
    user = relationship('User', primaryjoin=__table__.c.user_id==users.c.id)

class User(UserSchema):
    def writeable_by(self, user):
        return self.root or self.id == user.id

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

    def __json__(self):
        fields = ['email', 'first_name', 'middle_name', 'last_name', 'all_emails', 'tags',
            'classification', 'institution', 'department', 'international', 'notes']
        return dict((field, getattr(self, field, None)) for field in fields)
