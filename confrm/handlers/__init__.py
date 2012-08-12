from mako.exceptions import TopLevelLookupException
from pyramid.settings import asbool
from pyramid.response import Response
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPFound  # HTTPNotFound, HTTPUnauthorized
from confrm import redis
from confrm.lib import jsonize
from confrm.models import DBSession, UserSession, User
from confrm.exc import NotAuthorized, UnauthorizedHTTPMethod
import urllib


def error404(request):
    return HTTPFound(location='/users/index')


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self


class BaseHandler(object):
    format = 'mako'
    response = None

    def __init__(self, request):
        self.request = request
        self.ctx = AttrDict()
        self.ctx.debug = asbool(request.registry.settings['debug'])

        args = list(request.matchdict['args'])
        # self.path = [self.base, args[0]]
        if args[-1].endswith('.json'):
            self.format == 'json'
            args[-1] = args[-1].replace('.json', '')
        self.__route__(args)

    def __route__(self, args):
        getattr(self, args[0])(*args[1:])

    def json(self):
        json_string = jsonize(self.ctx)
        return Response(json_string, content_type='application/json')

    def __call__(self):
        if self.response:
            return self.response
        else:
            if self.format == 'json' or 'application/json' in str(self.request.accept):
                return self.json()
            try:
                return render_to_response('/%s.mako' % '/'.join(self.path), self.ctx, request=self.request)
            except TopLevelLookupException:
                # print 'Could not find mako, resorting to json.'
                return self.json()

    def set(self, **kw):
        self.ctx.update(kw)

    def flash(self, message, success=None):
        if 'flash' not in self.ctx:
            self.ctx.flash = []
        self.ctx.flash.append(dict(success=success, message=message))

    @property
    def user(self):
        ticket = self.request.cookies.get('ticket')
        cache_key = 'ticket_user_id.%s' % ticket
        user_id = redis.get(cache_key)
        if user_id:
            return DBSession.query(User).get(user_id)
        user_session = DBSession.query(UserSession).filter(UserSession.ticket == ticket).first()
        if user_session:
            redis.set(cache_key, user_session.user.id)
            return user_session.user
        return_url = urllib.quote_plus(self.request.path)
        raise HTTPFound(location='/user_sessions/new?flash=Please+sign+in+first.&url=%s' % return_url)

    def can_view(self, resource):
        if self.user.root:
            return True
        if not resource.viewable_by(self.user):
            raise NotAuthorized('Cannot view %s' % resource)

    def can_modify(self, resource):
        if self.request.method not in ['POST', 'PUT', 'DELETE']:
            raise UnauthorizedHTTPMethod('Cannot make modification unless using POST, PUT, or DELETE.')
        if self.user.root:
            return True
        if not resource.modifiable_by(self.user):
            raise NotAuthorized('Cannot modify %s' % resource)


class AuthenticatedHandler(BaseHandler):
    def __init__(self, request):
        super(AuthenticatedHandler, self).__init__(request)
        self.ctx.user = self.user
