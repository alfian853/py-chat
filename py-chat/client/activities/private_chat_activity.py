import os
import socket

from activities import AbstractActivity
from activities.activity_container import ActivityContainer


class PrivateChatActivity(AbstractActivity):
    instance = None

    def __init__(self, connection):
        super().__init__(connection)
        self.partner_user = None
        self.last_message = None
        self.last_file_name = None

    @staticmethod
    def get_instance(connection: socket.socket, container: ActivityContainer = None):
        if PrivateChatActivity.instance is None:
            PrivateChatActivity.instance = PrivateChatActivity(connection)
            PrivateChatActivity.instance.set_container(container)
        return PrivateChatActivity.instance

    def get_activity_input_line(self):
        return self.username + ' - ' + self.partner_user + '/Private Chat > '

    def show_menu(self):
        print('========Instruction=======')
        print('send <message>  # send message to friend')
        print('send_file <file_name>  # send a file to friend')
        print('get_file <kode_file> # get file based on unique code')
        print('======================\n')

    def init_chat_room(self, partner_username):
        self.partner_user = partner_username
        request = dict()
        request['COMMAND'] = 'MSG-PRIVATE-GET'
        request['p_username'] = partner_username
        self.send_request(request)

    def handle_input(self, args):
        args = args.split(' ', 1)
        print(args)
        request = dict()
        if args[0] == 'send':
            request['COMMAND'] = 'MSG-PRIVATE-SEND'
            request['message'] = args[1]
            self.send_request(request)
            self.last_message = args[1]

        elif args[0] == 'send_file':
            self.last_file_name = args[1]
            self._init_file_send_request()

        elif args[0] == 'get_file':
            self._init_get_file_request(args[1])
            pass
        elif args[0] == 'back':
            self.go_to_prev_activity()
        else:
            self.show_menu()

    def response_handler(self, response, is_json):
        if is_json:
            if response['FOR'] == 'MSG-PRIVATE-GET':
                for message in response['messages']:
                    print(message['from_user'] + ':', message['text'])
            elif response['FOR'] == 'MSG-PRIVATE-SEND':
                if response['status'] == 'success':
                    print(self.username + ':', self.last_message)
            elif response['FOR'] == 'NOTIF' \
                    and (response['from_user'] == self.partner_user
                         or response['from_user'] == self.username):
                print(response['from_user'] + ':', response['text'])
            elif response['FOR'] == 'FILE-PRIVATE-SEND':
                if response['status'] == 'ready':
                    self._send_file()
            elif response['FOR'] == 'FILE-PRIVATE-GET':
                if response['status'] == 'success':
                    self._download_file(response)
                else:
                    print(response['message'])
            else:
                print(response)

    def send_request(self, request):
        request['p_username'] = self.partner_user
        super().send_request(request)

    def _send_file(self):
        fd = open(self.last_file_name, 'rb')
        for data in fd:
            self.connection.sendall(data)
        print('===file sent!===')

    def _init_file_send_request(self):

        if not os.path.exists(self.last_file_name):
            print('file is not exist!')
            return

        request = dict()
        request['COMMAND'] = 'FILE-PRIVATE-SEND'
        request['p_username'] = self.partner_user
        request['file_name'] = self.last_file_name
        request['file_size'] = os.path.getsize(self.last_file_name)
        self.send_request(request)

    def _init_get_file_request(self, file_code):
        request = dict()
        request['COMMAND'] = 'FILE-PRIVATE-GET'
        request['file_code'] = file_code

        self.send_request(request)

    def _download_file(self, response):

        file_name = response['file_name']
        fd = open(file_name, 'wb+', 0)

        max_size = response['file_size']
        received = 0
        self.send_request({
            'status': 'ready'
        })
        while received < max_size:
            data = self.connection.recv(1024)
            received += len(data)
            fd.write(data)

        fd.close()

        print('==file downloaded==')
