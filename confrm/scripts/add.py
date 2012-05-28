#!/usr/bin/env python
import os
import sys
import transaction
from ConfigParser import ConfigParser
from confrm.lib import hash_password
from confrm.session import DBSession, metadata
from sqlalchemy import engine_from_config

argd = dict()
for arg1, arg2 in zip(sys.argv, sys.argv[1:]):
    if arg1.startswith('--'):
        key = arg1.replace('--', '')
        if arg2.startswith('--'):
            argd[key] = True
        else:
            argd[key] = arg2

config = ConfigParser(dict(here=os.getcwd()))
config.read([arg for arg in sys.argv if arg.endswith('.ini')][0])
app_config = dict(config.items('app:main'))

engine = engine_from_config(app_config)
DBSession.configure(bind=engine)
metadata.bind = engine

from confrm.models import Organization, User, OrganizationUser, Role

if 'email' in argd:
    user = User(email=argd['email'], password=hash_password(argd['password']))
    DBSession.add(user)
    DBSession.flush()
    print 'Added email'

if 'slug' in argd:
    org = Organization(slug=argd['slug'], name=argd['name'])
    DBSession.add(org)
    DBSession.flush()
    print 'Added organization'

if 'email' in argd and 'slug' in argd:
    role = DBSession.query(Role).filter(Role.name==u'superuser').first()
    org_user = OrganizationUser(user_id=user.id, organization_id=org.id, role_id=role.id, owns=True)
    DBSession.add(org_user)
    DBSession.flush()
    print 'Added user to organization'

transaction.commit()
