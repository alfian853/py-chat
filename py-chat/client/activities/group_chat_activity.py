import os
import socket

from activities import AbstractActivity
from activities.activity_container import ActivityContainer


class GroupChatActivity(AbstractActivity):
    instance = None

    def __init__(self, connection):
        super().__init__(connection)
        self.group_code = None
        self.group_name = None
        self.last_message = None
        self.last_file_name = None

    @staticmethod
    def get_instance(connection: socket.socket, container: ActivityContainer = None):
        if GroupChatActivity.instance is None:
            GroupChatActivity.instance = GroupChatActivity(connection)
            GroupChatActivity.instance.set_container(container)
        return GroupChatActivity.instance

    def get_activity_input_line(self):
        return self.username + ' - ' + self.group_name + '/Group Chat > '

    def show_menu(self):
        print('========Instruction=======')
        print('contact  # go to contact menu')
        print('group  # go to group menu')
        print('list  # get inbox')

    def init_chat_room(self, group_code):
        self.group_code = group_code
        request = dict()
        request['COMMAND'] = 'MSG-GROUP-GET'
        request['code'] = self.group_code
        self.send_request(request)

    def handle_input(self, args):
        args = args.split(' ', 1)
        request = dict()
        if args[0] == 'send':
            request['COMMAND'] = 'MSG-GROUP-SEND'
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

    def response_handler(self, response, is_json):

        if is_json:
            if response['FOR'] == 'MSG-GROUP-GET':
                for message in response['messages']:
                    print(message['from_user'] + ':', message['text'])

            elif response['FOR'] == 'MSG-GROUP-SEND':
                if response['status'] == 'success':
                    print(self.username + ':', self.last_message)

            elif response['FOR'] == 'NOTIF' and 'from_group' in response.keys()\
                    and response['from_group'] == self.group_name:
                print(response['from_user'] + ':', response['text'])

            elif response['FOR'] == 'FILE-GROUP-SEND':
                if response['status'] == 'ready':
                    self._send_file()

            elif response['FOR'] == 'FILE-GROUP-GET':
                if response['status'] == 'success':
                    self._download_file(response)
                else:
                    print(response['message'])
            else:
                print(response)

    def send_request(self, request):
        request['code'] = self.group_code
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
        request['COMMAND'] = 'FILE-GROUP-SEND'
        request['code'] = self.group_code
        request['file_name'] = self.last_file_name
        request['file_size'] = os.path.getsize(self.last_file_name)
        self.send_request(request)

    def _init_get_file_request(self, file_code):
        request = dict()
        request['COMMAND'] = 'FILE-GROUP-GET'
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
