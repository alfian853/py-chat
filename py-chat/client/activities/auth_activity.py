import socket

from activities import MenuActivity
from activities.abstract_activity import AbstractActivity
from activities.activity_container import ActivityContainer


class AuthActivity(AbstractActivity):

    instance = None

    def __init__(self, connection):
        super().__init__(connection)

    @staticmethod
    def get_instance(connection: socket.socket, container: ActivityContainer = None):
        if AuthActivity.instance is None:
            AuthActivity.instance = AuthActivity(connection)
            AuthActivity.instance.set_container(container)
        return AuthActivity.instance

    def get_activity_input_line(self):
        return 'Auth Menu > '

    def show_menu(self):
        print('auth page')
        print('login <username> <password>')
        print('register <username> <password> <retyped-password>')
        print('logout')

    def handle_input(self, args):
        args = args.split(' ', 2)

        request = dict()
        if args[0] == 'login':
            request['COMMAND'] = 'AUTH-LOGIN'
            request['username'] = args[1]
            request['password'] = args[2]

            self.send_request(request)
            response = self.get_response()

            if response['status'] == 'success':
                self.token = response['token']
                self.move_activity(MenuActivity.get_instance(self.connection, self.activity_container))

            print(response['message'])

        elif args[0] == 'register':
            request['COMMAND'] = 'AUTH-REGISTER'
            request['username'] = args[1]
            request['password'] = args[2]
            request['password-confirm'] = args[3]

            self.send_request(request)
            response = self.get_response()

            print(response['message'])

        elif args[0] == 'logout':
            request['COMMAND'] = 'AUTH-LOGOUT'

            self.send_request(request)
            response = self.get_response()

            if response['status'] == 'success':
                self.token = None

            print(response['message'])

        else:
            if args[0] != 'help':
                print('<UNKNOWN COMMAND>')
            self.show_menu()
            return

