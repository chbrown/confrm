import boto
from confrm.handlers import BaseHandler
from confrm.models import DBSession
from confrm.models.user import User, EventUser
from confrm.models.event import Event

class EventHandler(BaseHandler):
    base = 'events'

    def __route__(self, request):
        args = request.matchdict['args']
        self.path = [self.base, args[0]]
        getattr(self, args[0])(*args[1:])

    def index(self):
        events = DBSession.query(Event).all()
        self.ctx.events = events

    def new(self):
        pass

    def create(self):
        event = Event(self.request.POST)
        DBSession.add(event)
        DBSession.flush()

    def show(self, event_id):
        event = DBSession.query(Event).get(event_id)
        self.ctx.event = event

    def edit(self, event_id):
        event = DBSession.query(Event).get(event_id)
        self.ctx.event = event

    def update(self, event_id):
        event = DBSession.query(Event).get(event_id)
        self.ctx.event = event

    def delete(self, event_id):
        event = DBSession.query(Event).get(event_id)
        self.ctx.event = event

    def compose_email(self, event_id):
        self.ctx.from_users = DBSession.query(User).filter(User.email=='nasslli@nasslli2012.com').first()
        self.ctx.event = DBSession.query(Event).get(event_id)
        self.ctx.event_users = DBSession.query(EventUser).filter(EventUser.event_id==event_id)

    def send_email(self, event_id):
        # event = DBSession.query(Event).get(event_id)

        params = self.request.POST
        from_user = DBSession.query(User).get(params['from_user'])
        to_users = DBSession.query(User).filter(User.id.in_(params['to_users']))

        ses_conn = boto.connect_ses()
        ses_conn.send_email(from_user, params['subject'], params['body'], [to_user.full_email for to_user in to_users])
