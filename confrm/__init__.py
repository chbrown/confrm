from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from confrm.session import DBSession, metadata
session_factory = UnencryptedCookieSessionFactoryConfig('PZbjJ5U3phGt')

def main(global_config, **settings):
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    metadata.bind = engine

    config = Configurator(settings=settings, session_factory=session_factory)
    config.add_static_view('static', path='static/', cache_max_age=1)

    # User
    config.add_route('users', '/users/*args')
    config.add_view('confrm.handlers.users.UserHandler', route_name='users')
    config.add_route('user_sessions', '/user_sessions/*args')
    config.add_view('confrm.handlers.user_sessions.UserSessionHandler', route_name='user_sessions')
    config.add_route('files', '/groups/{group_id}/files/*args')
    config.add_view('confrm.handlers.files.FileHandler', route_name='files')

    # per-Org
    config.add_route('groups', '/{organization}/groups/*args')
    config.add_view('confrm.handlers.organization.groups.GroupHandler', route_name='groups')

    config.add_notfound_view('confrm.handlers.error404')
    config.add_route('root', '/')

    return config.make_wsgi_app()
