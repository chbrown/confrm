from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from confrm.models import DBSession  # , metadata


def main(global_config, **settings):
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    # metadata.bind = engine

    config = Configurator(settings=settings)
    config.add_static_view('static', path='static/', cache_max_age=1)

    config.add_route('users', '/users/*args')
    config.add_view('confrm.handlers.users.UserHandler', route_name='users')

    config.add_notfound_view('confrm.handlers.root404')
    config.add_route('root', '/')

    return config.make_wsgi_app()
