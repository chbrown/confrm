from confrm.handlers import BaseHandler
from confrm.models import DBSession
from confrm.models.user import Event

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
        event = DBSession.query(Event).get(event_id)

        self.ctx.event = event
        self.ctx.event_users = event.users

    def send_email(self, event_id):
        event = DBSession.query(Event).get(event_id)

        subject = self.request.POST['body']
        body = self.request.POST['body']
        users = self.request.POST['users']
        for user in users:
            ses_conn.send_email('audiere@gmail.com', 'hey chb', body, ['io@henrian.com'])
