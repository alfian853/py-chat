import socket
import json


class AbstractActivity(object):
    token = None
    connection: socket.socket = None
    activity_container = None

    def __init__(self, connection, container = None):
        self.connection = connection
        self.activity_container = container

    def set_container(self, container):
        self.activity_container = container

    def handle_input(self, args):
        print('unhandled input:', args)

    def get_activity_input_line(self):
        return '> '

    def show_menu(self):
        print('menu :')

    def send_request(self, response):
        if isinstance(response, dict):
            response['token'] = self.token
            self.connection.sendall(json.dumps(response).encode('utf-8'))
        else:
            self.connection.sendall(response.encode('utf-8'))

    def get_response(self):
        return json.loads(self.connection.recv(1024).decode('utf-8'))

    def get_response_bytes(self):
        return self.connection.recv(1024).decode('utf-8')

    def move_activity(self, target_activity):
        if self.activity_container is not None:
            self.activity_container.set_activity(target_activity)
        else:
            print('activity container not assigned!')
