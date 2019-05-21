import socket

from activities.abstract_activity import AbstractActivity
from activities.activity_container import ActivityContainer
from activities.private_chat_activity import PrivateChatActivity


class ContactActivity(AbstractActivity):

    instance = None

    @staticmethod
    def get_instance(connection: socket.socket, container: ActivityContainer = None):
        if ContactActivity.instance is None:
            ContactActivity.instance = ContactActivity(connection)
            ContactActivity.instance.set_container(container)
        return ContactActivity.instance

    def get_activity_input_line(self):
        return 'Contact Menu > '

    def show_menu(self):
        print('========Instruction=======')
        print('get  # show list of contact')
        print('add <username>  # add to contact')
        print('del <username> # delete from contact')
        print('chat <username> # go to personal chat room with user')

    def handle_input(self, args: str):
        args = args.split(' ')
        request = dict()
        if args[0] == 'get':
            request['COMMAND'] = 'CONTACT-GET'
            self.send_request(request)

        elif args[0] == 'add':
            self._add_contact(args)

        elif args[0] == 'del':
            self._del_contact(args)

        elif args[0] == 'chat':
            next_activity = PrivateChatActivity.get_instance(self.connection, self.activity_container)
            next_activity.set_from_activity(self)
            next_activity.init_chat_room(args[1])
            self.move_activity(next_activity)

        elif args[0] == 'back':
            self.go_to_prev_activity()

    def _add_contact(self, args: list):
        request = dict()
        request['COMMAND'] = 'CONTACT-ADD'
        request['contact_list'] = args[1:]
        self.send_request(request)

    def _del_contact(self, args: list):
        request = dict()
        request['COMMAND'] = 'CONTACT-DEL'
        request['contact_list'] = args[1:]
        self.send_request(request)

    def response_handler(self, response, is_json):
        if is_json:
            if response['FOR'] == 'CONTACT-GET':
                contacts = response['contact_list']
                i = 1
                for contact in contacts:
                    print(str(i)+'.', contact)
                    i += 1
            else:
                print(response['message'])

