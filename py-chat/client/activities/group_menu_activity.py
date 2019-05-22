import socket
import sys

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
        print('join <group_code> # join to group with code')
        print('invite <group_code> <friend_username 1..N> # invite friend to join group')
        print('get  # get numbered list of joined group')
        print('chat <group order number in list> enter group chat room')
        print('exit <group_code> # leave group')
        print('back # back to main menu')
        print('==============================\n')

    def handle_input(self, args: str):
        args = args.split(' ')

        if args[0] == 'create':

            self.send_request({
                'COMMAND': 'GROUP-CREATE',
                'group_name': ' '.join(args[1:])
            })

        elif args[0] == 'get':
            self.send_request({
                'COMMAND': 'GROUP-GET'
            })

        elif args[0] == 'join':
            self.send_request({
                'COMMAND': 'GROUP-JOIN',
                'code': args[1]
            })

        elif args[0] == 'chat':
            if int(args[1]) >= len(self.groups):
                print('invalid group number')
                return

            group = self.groups[int(args[1])]
            next_activity = GroupChatActivity.get_instance(self.connection, self.activity_container)
            next_activity.group_name = group['group_name']
            next_activity.group_code = group['code']
            next_activity.init_chat_room(group['code'])
            next_activity.set_from_activity(self)
            self.move_activity(next_activity)

        elif args[0] == 'invite':
            self.send_request({
                'COMMAND': 'GROUP-INVITE',
                'code': args[1],
                'user_list': args[2:]
            })
        elif args[0] == 'exit':
            self.send_request({
                'COMMAND': 'GROUP-EXIT',
                'code': args[1]
            })
        elif args[0] == 'back':
            self.go_to_prev_activity()
        else:
            self.show_menu()

    def response_handler(self, response, is_json):

        if is_json:
            if response['FOR'] == 'GROUP-GET':
                groups = response['group_list']
                self.groups = groups
                if len(groups) == 0:
                    print('you are not joined to any group')
                # i = 1
                for i in range(len(groups)):
                    # print(str(i)+'.', group['group_name'])
                    print("{}. {}".format(i, groups[i]))
                    # i += 1
            else:
                super().response_handler(response, is_json)

