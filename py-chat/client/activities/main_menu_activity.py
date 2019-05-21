import socket

from activities.activity_container import ActivityContainer
from activities import ContactActivity, AbstractActivity


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

    def handle_input(self, args):
        args = args.split(' ')

        if args[0] == 'contact':
            next_activity = ContactActivity.get_instance(self.connection, self.activity_container)
            print('move ', next_activity.__class__)
            self.move_activity(next_activity)
            next_activity.set_from_activity(self)
        elif args[0] == 'back':
            self.go_to_prev_activity()

