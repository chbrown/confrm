from pyramid.settings import asbool
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
import redis as redis_lib
redis = redis_lib.StrictRedis()

from confrm.session import DBSession, metadata


def main(global_config, **settings):
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    metadata.bind = engine

    config = Configurator(settings=settings)

    if asbool(settings['debug']):
        config.add_static_view('static', path='static/', cache_max_age=1)
        config.add_static_view('css', path='static/css/', cache_max_age=1)
        config.add_static_view('img', path='static/img/', cache_max_age=1)
        config.add_static_view('js', path='static/js/', cache_max_age=1)
        config.add_static_view('templates', path='templates/', cache_max_age=1)

    # User
    config.add_route('users', '/users*args')
    config.add_view('confrm.handlers.users.UserHandler', route_name='users')
    config.add_route('user_sessions', '/user_sessions*args')
    config.add_view('confrm.handlers.user_sessions.UserSessionHandler', route_name='user_sessions')
    config.add_route('files', '/files*args')
    config.add_view('confrm.handlers.files.FileHandler', route_name='files')
    config.add_route('groups', '/groups*args')
    config.add_view('confrm.handlers.groups.GroupHandler', route_name='groups')

    config.add_notfound_view('confrm.handlers.error404')
    config.add_route('root', '/')

    return config.make_wsgi_app()
