from confrm.models import DeclarativeBase
from confrm.models.tables import users, messages

class Message(DeclarativeBase):
    __table__ = messages
