from confrm.models import BaseModel
from confrm.models.tables import users, messages

class Message(BaseModel):
    __table__ = messages
