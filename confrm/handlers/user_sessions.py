from confrm.handlers import BaseHandler
from confrm.models import DBSession
from confrm.models.user import User, UserSession
from confrm.lib import random_ticket


class UserSessionHandler(BaseHandler):
    path = ('user_sessions',)

    def new(self):
        pass

    def create(self):
        email = self.request.json_body.get('email')
        password = self.request.json_body.get('password', '')

        password_hash = User.hash_password(email, password)

        user = DBSession.query(User).filter(User.email==email).filter(User.password==password_hash).first()
        if user:
            ticket = random_ticket()
            user_session = UserSession(user_id=user.id, ticket=ticket)
            DBSession.add(user_session)
            self.set(success=True, message='Logged in.', ticket=ticket)
        else:
            self.set(success=False, message='Authentication failed, please try again.')

    # def update(self, user_id):
        # user = DBSession.query(User).get(user_id)
        # if user ==
