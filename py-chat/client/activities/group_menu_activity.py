import socket

from activities import AbstractActivity, GroupChatActivity
from activities.activity_container import ActivityContainer


class GroupMenuActivity(AbstractActivity):

    instance = None

    @staticmethod
    def get_instance(connection: socket.socket, container: ActivityContainer = None):
        if GroupMenuActivity.instance is None:
            GroupMenuActivity.instance = GroupMenuActivity(connection)
            GroupMenuActivity.instance.set_container(container)
        return GroupMenuActivity.instance

    def __init__(self, connection):
        super().__init__(connection)
        self.groups = []

    def get_activity_input_line(self):
        return 'Group Menu > '

    def init_group_menu_data(self):
        self.send_request({
            'COMMAND': 'GROUP-GET'
        })

    def show_menu(self):
        print('========Instruction=======')
        print('create <group_name>  # create a group')
        print('get  # get numbered list of joined group')
        print('chat <group order number in list> enter group chat room')
        print('back # back to main menu')
        print('==============================\n')

    def handle_input(self, args: str):
        args = args.split(' ')

        if args[0] == 'create':
            pass

        elif args[0] == 'get':
            self.send_request({
                'COMMAND': 'GROUP-GET'
            })

        elif args[0] == 'chat':
            if int(args[1]) >= len(self.groups):
                print('invalid group number')
                return

            group = self.groups[int(args[1])]
            next_activity = GroupChatActivity.get_instance(self.connection, self.activity_container)
            next_activity.group_name = group['group_name']
            next_activity.group_id = group['id']
            next_activity.init_chat_room(group['id'])
            next_activity.set_from_activity(self)
            self.move_activity(next_activity)

        elif args[0] == 'add':
            self.send_request({
                'COMMAND': 'GROUP-INVITE',
                'user_list': args[1:]
            })
        elif args[0] == 'back':
            self.go_to_prev_activity()

        else:
            self.show_menu()

    def response_handler(self, response, is_json):

        if is_json:
            if response['FOR'] == 'GROUP-GET':
                self.groups = response['group_list']
                i = 0
                for group in self.groups:
                    print(str(i)+'.', group['group_name'])
            elif response['FOR'] == 'GROUP-INVITE':
                print(response['message'])
