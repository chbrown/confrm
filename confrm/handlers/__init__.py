from mako.exceptions import TopLevelLookupException
from pyramid.response import Response
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPFound  # HTTPNotFound, HTTPUnauthorized
from confrm.lib import jsonize
from confrm.models import DBSession, UserSession

def error404(request):
    return HTTPFound(location='/users/index')

class NotAuthorized(Exception):
    pass

class UnauthorizedHTTPMethod(Exception):
    pass

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

        args = list(request.matchdict['args'])
        self.path = [self.base, args[0]]
        if args[-1].endswith('.json'):
            self.format == 'json'
            args[-1] = args[-1].replace('.json', '')
        self.__route__(args)

    def __route__(self, args):
        getattr(self, args[0])(*args[1:])

    def __json__(self):
        json_string = jsonize(self.ctx)
        return Response(json_string, content_type='application/json')

    def __call__(self):
        if self.format == 'json':
            return self.__json__()
        try:
            return render_to_response('/%s.mako' % '/'.join(self.path), self.ctx, request=self.request)
        except TopLevelLookupException:
            print 'Could not find mako, resorting to json.'
            return self.__json__()

    def set_ctx(self, **kw):
        self.ctx.update(kw)

    def flash(self, message, success=None):
        if 'flash' not in self.ctx:
            self.ctx.flash = []
        self.ctx.flash.append(dict(success=success, message=message))

    @property
    def user(self):
        ticket = self.request.cookies.get('ticket')
        user_session = DBSession.query(UserSession).filter(UserSession.ticket==ticket).first()
        if user_session:
            return user_session.user
        raise HTTPFound(location='/user_sessions/new?flash=Please+sign+in+first.')

    def can_view(self, resource):
        if not resource.viewable_by(self.user):
            raise NotAuthorized('Cannot view %s' % resource)

    def can_modify(self, resource):
        if self.request.method not in ['POST', 'PUT', 'DELETE']:
            raise UnauthorizedHTTPMethod('Cannot make modification unless using POST, PUT, or DELETE.')
        return resource.modifiable_by(self.user)
