from sqlalchemy.orm import relationship
from confrm.models import BaseModel
from confrm.models.tables import users, organizations, organizations_users

class Organization(BaseModel):
    __table__ = organizations

class OrganizationUser(BaseModel):
    __table__ = organizations_users
    organization = relationship('Organization', primaryjoin=__table__.c.organization_id==organizations.c.id)
    user =         relationship('User',         primaryjoin=__table__.c.user_id==users.c.id)
    created_by =   relationship('User',         primaryjoin=__table__.c.created_by_id==users.c.id)
    archived_by =  relationship('User',         primaryjoin=__table__.c.archived_by_id==users.c.id)
    deleted_by =   relationship('User',         primaryjoin=__table__.c.deleted_by_id==users.c.id)
