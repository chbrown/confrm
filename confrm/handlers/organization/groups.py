import boto
from confrm.handlers import BaseHandler
from confrm.models import DBSession, User, Group, GroupUser

class GroupHandler(BaseHandler):
    base = 'groups'

    def __route__(self, request):
        args = request.matchdict['args']
        self.path = [self.base, args[0]]
        getattr(self, args[0])(*args[1:])

    def index(self):
        groups = DBSession.query(Group).all()
        self.ctx.groups = groups

    def new(self):
        pass

    def create(self):
        group = Group(self.request.POST)
        DBSession.add(group)
        DBSession.flush()

    def show(self, group_id):
        group = DBSession.query(Group).get(group_id)
        self.ctx.group = group

    def edit(self, group_id):
        group = DBSession.query(Group).get(group_id)
        self.ctx.group = group

    def update(self, group_id):
        group = DBSession.query(Group).get(group_id)
        self.ctx.group = group

    def delete(self, group_id):
        group = DBSession.query(Group).get(group_id)
        self.ctx.group = group

    def compose_email(self, group_id):
        self.ctx.from_users = DBSession.query(User).filter(User.email=='nasslli@nasslli2012.com').first()
        self.ctx.group = DBSession.query(Group).get(group_id)
        self.ctx.group_users = DBSession.query(GroupUser).filter(GroupUser.group_id==group_id)

    def send_email(self, group_id):
        # group = DBSession.query(Group).get(group_id)

        params = self.request.POST
        from_user = DBSession.query(User).get(params['from_user'])
        to_users = DBSession.query(User).filter(User.id.in_(params['to_users']))

        ses_conn = boto.connect_ses()
        ses_conn.send_email(from_user, params['subject'], params['body'], [to_user.full_email for to_user in to_users])
