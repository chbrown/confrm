from confrm.handlers import BaseHandler

class OrganizationHandler(BaseHandler):
    def __route__(self, args):
        self.path = ['organizations', args[0]]
        getattr(self, args[0])(*args[1:])
