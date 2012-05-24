from pyramid.response import Response
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPFound  # HTTPNotFound, HTTPUnauthorized
from confrm.lib import site
import json


def error404(request):
    return HTTPFound(location='/users/index')


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self


class BaseHandler(object):
    ctx = None
    format = 'mako'

    def __init__(self, request):
        self.request = request
        self.ctx = AttrDict(site=site)
        self.__route__(request)

    def __call__(self):
        if self.format == 'json':
            return Response(json.dumps(self.ctx), content_type='application/json')
        return render_to_response('/%s.mako' % '/'.join(self.path), self.ctx, request=self.request)

    def set(self, dictionary):
        self.ctx.update(dictionary)
