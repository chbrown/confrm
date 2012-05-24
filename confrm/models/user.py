from sqlalchemy import Table
from sqlalchemy.orm import relationship
from confrm import DBSession
from confrm.models import metadata, DeclarativeBase

users_table = Table('users', metadata, autoload=True)
user_sessions_table = Table('user_sessions', metadata, autoload=True)

class Role(DeclarativeBase):
    __table__ = Table('roles', metadata, autoload=True)

class UserSchema(DeclarativeBase):
    __table__ = users_table
    created_by  = relationship('User')  # , primaryjoin=__table__.c.created_by==users_table.c.id)
    deleted_by  = relationship('User')  # , primaryjoin=__table__.c.deleted_by==users_table.c.id)
    archived_by = relationship('User')  # , primaryjoin=__table__.c.archived_by==users_table.c.id)
    role = relationship('Role')

class Event(DeclarativeBase):
# class Event(EventSchema):
# class EventSchema(DeclarativeBase):
    __table__ = Table('events', metadata, autoload=True)
    created_by  = relationship('User')  # , primaryjoin=__table__.c.created_by==users_table.c.id)
    deleted_by  = relationship('User')  # , primaryjoin=__table__.c.deleted_by==users_table.c.id)
    archived_by = relationship('User')  # , primaryjoin=__table__.c.archived_by==users_table.c.id)

class EventUser(DeclarativeBase):
    __table__ = Table('events_users', metadata, autoload=True)
    event = relationship('Event')
    user = relationship('User')
    created_by  = relationship('User')
    deleted_by  = relationship('User')

class UserSession(DeclarativeBase):
    __table__ = user_sessions_table

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
