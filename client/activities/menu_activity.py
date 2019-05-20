import socket

from activities.abstract_activity import AbstractActivity
from activities.activity_container import ActivityContainer


class MenuActivity(AbstractActivity):

    instance = None

    def __init__(self, connection):
        super().__init__(connection)

    @staticmethod
    def get_instance(connection: socket.socket, container: ActivityContainer = None):
        if MenuActivity.instance is None:
            MenuActivity.instance = MenuActivity(connection)
            MenuActivity.instance.set_container(container)
        return MenuActivity.instance

    def handle_input(self, args):
        print('menu input')

    def get_activity_input_line(self):
        return 'Main Menu > '






