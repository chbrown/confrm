from confrm.models import DeclarativeBase
from confrm.models.tables import roles

class Role(DeclarativeBase):
    __table__ = roles
