import socket
import json


class AbstractActivity(object):
    token = None
    username = None
    connection: socket.socket = None
    activity_container = None

    def __init__(self, connection, container = None):
        self.connection = connection
        self.activity_container = container
        self.from_activity = None

    def set_token(self, token):
        AbstractActivity.token = token

    def set_username(self, username):
        AbstractActivity.username = username

    def set_container(self, container):
        self.activity_container = container

    def set_from_activity(self, from_activity):
        self.from_activity = from_activity

    def go_to_prev_activity(self):
        self.move_activity(self.from_activity)

    def handle_input(self, args: str):
        print('unhandled input:', args)

    def get_activity_input_line(self):
        return '> '

    def show_menu(self):
        print('menu :')

    def send_request(self, request):
        if isinstance(request, dict):
            request['token'] = AbstractActivity.token
            self.connection.sendall(json.dumps(request).encode('utf-8'))
        else:
            self.connection.sendall(request.encode('utf-8'))

    def get_response(self):
        return json.loads(self.connection.recv(1024).decode('utf-8'))

    def get_response_bytes(self):
        return self.connection.recv(1024).decode('utf-8')

    def move_activity(self, target_activity):
        if self.activity_container is not None:
            self.activity_container.set_activity(target_activity)
        else:
            print('activity container not assigned!')
        print(self.get_activity_input_line())

    def get_connection(self):
        return self.connection

    def response_handler(self, response, is_json):
        if is_json:
            if response['FOR'] == 'NOTIF':
                if 'from_group' in response.keys():
                    print('[New Message from '+response['from_user']+' ('+response['from_group']+')]:', response['text'])
                else:
                    print('[New Message from '+response['from_user']+']:', response['text'])
            else:
                print('unhandled response')
        else:
            print('unhandled bytes response')
