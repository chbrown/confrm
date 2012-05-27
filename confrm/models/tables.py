from sqlalchemy import Table
from confrm.models import metadata

tables = ['roles', 'organizations', 'users', 'user_sessions', 'organizations_users',
    'groups', 'groups_users', 'files', 'files_groups', 'files_users', 'messages']
for table in tables:
    vars()[table] = Table(table, metadata, autoload=True)

__all__ = tables
