# from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from confrm.session import DBSession, metadata
# session_factory = UnencryptedCookieSessionFactoryConfig('PZbjJ5U3phGt')

def main(global_config, **settings):
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    metadata.bind = engine

    config = Configurator(settings=settings)
    config.add_static_view('static', path='static/', cache_max_age=1)

    # User
    config.add_route('users', '/users/*args')
    config.add_view('confrm.handlers.users.UserHandler', route_name='users')
    config.add_route('user_sessions', '/user_sessions/*args')
    config.add_view('confrm.handlers.user_sessions.UserSessionHandler', route_name='user_sessions')
    config.add_route('files', '/files/*args')
    config.add_view('confrm.handlers.files.FileHandler', route_name='files')
    config.add_route('groups', '/groups/*args')
    config.add_view('confrm.handlers.groups.GroupHandler', route_name='groups')

    config.add_notfound_view('confrm.handlers.error404')
    config.add_route('root', '/')

    return config.make_wsgi_app()
