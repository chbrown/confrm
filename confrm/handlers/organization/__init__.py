import json
from mako.exceptions import TopLevelLookupException
from pyramid.response import Response
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPFound  # HTTPNotFound, HTTPUnauthorized
from confrm.models import UserSession

def error404(request):
    return HTTPFound(location='/users/index')

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        custom_json_function = getattr(obj, '__json__', None)
        if custom_json_function:
            return custom_json_function()
        return super(CustomEncoder, self).default(self, obj)

custom_encoder = CustomEncoder()

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self


class BaseHandler(object):
    ctx = None
    format = 'mako'

    def __init__(self, request):
        self.request = request
        self.ctx = AttrDict()
        self.__route__(request)

    def __route__(self, request):
        args = request.matchdict['args']
        self.path = [self.base, args[0]]
        getattr(self, args[0])(*args[1:])

    def __json__(self):
        json_string = custom_encoder.encode(self.ctx)
        return Response(json_string, content_type='application/json')

    def __call__(self):
        if self.format == 'json':
            return self.__json__()
        try:
            return render_to_response('/%s.mako' % '/'.join(self.path), self.ctx, request=self.request)
        except TopLevelLookupException:
            return self.__json__()

    def set_ctx(self, **kw):
        self.ctx.update(kw)

    def flash(self, message, success=None):
        if 'flash' not in self.ctx:
            self.ctx.flash = []
        self.ctx.flash.append(dict(success=success, message=message))

    @property
    def user(self):
        ticket = self.request.session.get('ticket')
        user_session = UserSession.filter(UserSession.ticket==ticket).first()
        if user_session:
            return user_session.user

    def can_view(self, resource):
        self.user.can
        pass

    def can_modify(self, resource):
        if self.request.method not in ['POST', 'PUT']:
            raise Exception('Cannot make modification unless using POST or PUT.')
