from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from confrm.models import DBSession, metadata
from confrm.lib import site


def main(global_config, **settings):
    engine = engine_from_config(settings, 'sqlalchemy.')
    site.name = settings['name']
    DBSession.configure(bind=engine)
    metadata.bind = engine

    config = Configurator(settings=settings)
    config.add_static_view('static', path='static/', cache_max_age=1)

    config.add_route('users', '/users/*args')
    config.add_view('confrm.handlers.users.UserHandler', route_name='users')

    config.add_route('user_sessions', '/user_sessions/*args')
    config.add_view('confrm.handlers.user_sessions.UserSessionHandler', route_name='user_sessions')

    config.add_route('uploads', '/uploads/*args')
    config.add_view('confrm.handlers.uploads.UploadHandler', route_name='uploads')

    config.add_notfound_view('confrm.handlers.error404')
    config.add_route('root', '/')

    return config.make_wsgi_app()
