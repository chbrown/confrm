from sqlalchemy.orm import relationship
from confrm.models import DeclarativeBase, DBSession
from confrm.models.tables import users, user_sessions, events, events_users, roles
from confrm.models.event import Event
from confrm.models.role import Role

class UserSchema(DeclarativeBase):
    __table__ = users
    created_by  = relationship('User', primaryjoin=__table__.c.created_by_id==users.c.id)
    deleted_by  = relationship('User', primaryjoin=__table__.c.deleted_by_id==users.c.id)
    archived_by = relationship('User', primaryjoin=__table__.c.archived_by_id==users.c.id)
    role = relationship(Role,          primaryjoin=__table__.c.role_id==roles.c.id)

class EventUser(DeclarativeBase):
    __table__ = events_users
    event = relationship(Event,       primaryjoin=__table__.c.event_id==events.c.id)
    user = relationship('User',       primaryjoin=__table__.c.user_id==users.c.id)
    role = relationship(Role,         primaryjoin=__table__.c.role_id==roles.c.id)
    created_by = relationship('User', primaryjoin=__table__.c.created_by_id==users.c.id)
    deleted_by = relationship('User', primaryjoin=__table__.c.deleted_by_id==users.c.id)

class UserSession(DeclarativeBase):
    __table__ = user_sessions

class User(UserSchema):
    def event_role(self, event_id):
        return DBSession.query(EventUser).filter(EventUser.event_id==event_id).filter(EventUser.user_id==self.id).first()

    def can_edit(self, resource):
        if isinstance(resource, User):
            return self.role in ['superuser', 'admin'] or self == resource
        elif isinstance(resource, Event):
            return self.event_role(resource.id) in ['superuser', 'admin', 'teacher']
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
