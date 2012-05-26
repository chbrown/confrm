from sqlalchemy.orm import relationship
from confrm.models import DeclarativeBase
from confrm.models.tables import users, events

class Event(DeclarativeBase):
    __table__ = events
    created_by  = relationship('User', primaryjoin=__table__.c.created_by_id==users.c.id)
    deleted_by  = relationship('User', primaryjoin=__table__.c.deleted_by_id==users.c.id)
    archived_by = relationship('User', primaryjoin=__table__.c.archived_by_id==users.c.id)
