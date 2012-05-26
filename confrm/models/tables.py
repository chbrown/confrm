from sqlalchemy import Table
from confrm.models import metadata

roles = Table('roles', metadata, autoload=True)
users = Table('users', metadata, autoload=True)
user_sessions = Table('user_sessions', metadata, autoload=True)
events = Table('events', metadata, autoload=True)
events_users = Table('events_users', metadata, autoload=True)
