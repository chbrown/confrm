from pyramid.response import Response
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPFound  # HTTPNotFound, HTTPUnauthorized
from confrm.lib import site
import json
from mako.exceptions import TopLevelLookupException

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
        self.ctx = AttrDict(site=site)
        self.__route__(request)

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

    def set(self, dictionary):
        self.ctx.update(dictionary)

    def flash(self, message, success=None):
        if 'flash' not in self.ctx:
            self.ctx.flash = []
        self.ctx.flash.append(dict(success=success, message=message))
