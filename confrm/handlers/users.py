# from pyramid.response import Response
from confrm.handlers import BaseHandler
from confrm.models import DBSession
from confrm.models.user import User

class UserHandler(BaseHandler):
    base = 'users'

    def __route__(self, request):
        # super(UserHandler, self).__init__(request)
        # return Response('hi')

        args = request.matchdict['args']
        self.path = [self.base, args[0]]
        getattr(self, args[0])(*args[1:])

    def index(self):
        # self.parts.append('index')
        # .filter(User.name == 'one')
        users = DBSession.query(User).all()
        self.ctx.users = users


    # from sqlalchemy.exc import DBAPIError
    # except DBAPIError:
    #     return Response("DB error message", content_type='text/plain', status_int=500)
