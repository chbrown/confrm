from sqlalchemy import Table
from sqlalchemy.orm import relationship
from confrm.models import DeclarativeBase, metadata

users_table = Table('users', metadata, autoload=True)

class Event(DeclarativeBase):
    __table__ = Table('events', metadata, autoload=True)
    created_by  = relationship('User', primaryjoin=__table__.c.created_by_id==users_table.c.id)
    deleted_by  = relationship('User', primaryjoin=__table__.c.deleted_by_id==users_table.c.id)
    archived_by = relationship('User', primaryjoin=__table__.c.archived_by_id==users_table.c.id)
