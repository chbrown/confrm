from confrm.handlers import BaseHandler
from confrm.models import DBSession
from confrm.models.user import User, UserSession
from confrm.lib import hash_password, random_ticket

class UserSessionHandler(BaseHandler):
    def create(self):
        email = self.request.POST.get('email')
        password = self.request.POST.get('password')

        password_hash = hash_password(password)

        user = DBSession.query(User).filter(User.email==email).filter(User.password==password_hash).first()
        if user:
            ticket = random_ticket()
            user_session = UserSession(user_id=user.id, ticket=ticket)
            DBSession.add(user_session)
            self.ctx.set(success=True, message='Logged in.', ticket=ticket)
        else:
            self.ctx.set(success=False, message='Authenticiation failed.')

    # def update(self, user_id):
        # user = DBSession.query(User).get(user_id)
        # if user ==
