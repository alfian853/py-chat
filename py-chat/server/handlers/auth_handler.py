import uuid

from entities import UserEntity
from handlers import AbstractHandler
from repositories import UserRepository
from session import Session


# untuk auth user sebelum masuk ke core service
class AuthHandler(AbstractHandler):
    instance = None

    @staticmethod
    def get_instance():
        if AuthHandler.instance is None:
            AuthHandler.instance = AuthHandler()
        return AuthHandler.instance

    def __init__(self):
        super().__init__()
        self.tokens_data = {}
        self.repository = UserRepository.get_instance()

    def handle(self, session, request):
        command: str = request['COMMAND']
        # print(request)
        if command is None:
            session.send_response({
                'FOR': request['COMMAND'],
                'status': 'failed',
                'message': 'unknown request format!'
            })
        print('is auth : ',self._is_authenticated(session, request))
        sub_command = command.split('-')
        if sub_command[0] == 'AUTH':
            task = sub_command[1]
            print(task)
            if task == 'LOGIN':
                self._do_login(session, request)
            if task == 'LOGOUT':
                self._do_logout(session, request)
            if task == 'REGISTER':
                self._do_register(session, request)
        elif self._is_authenticated(session, request):
            super(AuthHandler, self).handle(session, request)
        else:
            session.send_response({
                'status': 'failed',
                'message': 'unauthorized!'
            })

    def _is_authenticated(self, session: Session, request):
        """
        :param request: dict
        :return:
        """
        if 'token' not in request.keys():
            return False

        token = request['token']

        if token is None or token is '':
            return False

        return session.token == token

    def _do_login(self, session: Session, request):
        """
        :param _socket.socket connection:
        :param request:
        :return:
        """
        print('do login')
        username = request['username']
        password = request['password']
        if username is None or password is None:
            session.send_response({
                'FOR': 'AUTH-LOGIN',
                'status': 'failed',
                'message': 'username or password can\'t be empty'
            })

        user = self.repository.find_by_username(username)

        if user is None:
            session.send_response({
                'FOR': request['COMMAND'],
                'status': 'failed',
                'message': 'unknown user'
            })

        if user.password == password:
            session.set_login_user(user)
            session.token = str(uuid.uuid4())
            session.send_response({
                'FOR': request['COMMAND'],
                'status': 'success',
                'message': 'you are logged in now',
                'token': session.token
            })
        else:
            session.send_response({
                'FOR': request['COMMAND'],
                'status': 'failed',
                'message': 'wrong password'
            })

    def _do_logout(self, session: Session, request):
        if self._is_authenticated(session, request):
            session.clear()
            session.send_response({
                'FOR': request['COMMAND'],
                'status': 'success',
                'message': 'you are logged out now'
            })
        else:
            session.send_response({
                'FOR': request['COMMAND'],
                'status': 'failed',
                'message': 'unauthorized request!'
            })

    def _do_register(self, session: Session, request):
        username = request['username']
        password1 = request['password']
        password2 = request['password-confirm']

        if username is None or password1 is None or password2 is None:
            session.send_response({
                'FOR': request['COMMAND'],
                'status': 'failed',
                'message': 'please provide \'username\',\'password\',\'password-confirm\''
            })

        if password1 != password2:
            session.send_response({
                'FOR': request['COMMAND'],
                'status': 'failed',
                'message': 'password doesn\'t match!'
            })

        user = self.repository.find_by_username(username)

        if user is None:
            user = UserEntity()
            user.username = username
            user.password = password1
            self.repository.save(user)
            session.send_response({
                'FOR': request['COMMAND'],
                'status': 'success',
                'message': 'you are registered now!'
            })
        else:
            session.send_response({
                'FOR': request['COMMAND'],
                'status': 'failed',
                'message': 'that username already been used'
            })
