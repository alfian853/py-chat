import socket

from activities.activity_container import ActivityContainer
from activities import ContactActivity, AbstractActivity,GroupMenuActivity


class MainMenuActivity(AbstractActivity):
    instance = None

    def __init__(self, connection):
        super().__init__(connection)

    @staticmethod
    def get_instance(connection: socket.socket, container: ActivityContainer = None):
        if MainMenuActivity.instance is None:
            MainMenuActivity.instance = MainMenuActivity(connection)
            MainMenuActivity.instance.set_container(container)
        return MainMenuActivity.instance

    def get_activity_input_line(self):
        return self.username + '/Main Menu > '

    def show_menu(self):
        print('========Instruction=======')
        print('contact  # go to contact menu')
        print('group  # go to group menu')
        print('list  # get inbox')
        print('back # back to auth')
        print('==============================\n')

    def handle_input(self, args):
        args = args.split(' ')

        if args[0] == 'contact':
            next_activity = ContactActivity.get_instance(self.connection, self.activity_container)
            self.move_activity(next_activity)
            next_activity.set_from_activity(self)

        elif args[0] == 'group':
            next_activity = GroupMenuActivity.get_instance(self.connection, self.activity_container)
            next_activity.init_group_menu_data()
            next_activity.set_from_activity(self)
            self.move_activity(next_activity)

        elif args[0] == 'back':
            self.go_to_prev_activity()

        else:
            self.show_menu()

