from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError
from confrm.models import DBSession, MyModel


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    try:
        one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response("DB error message", content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'confrm'}
