from sqlalchemy import Table
from confrm.models import DeclarativeBase, metadata

class Role(DeclarativeBase):
    __table__ = Table('roles', metadata, autoload=True)
