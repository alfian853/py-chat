import socket
import threading

from activities.activity_container import ActivityContainer
from activities import AuthActivity
from env import Env


class Client(threading.Thread):

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_addr = ('127.0.0.1', Env.server_port)
        self.sock.connect(server_addr)
        print('connected to '+str(server_addr))

        self.activity_container = ActivityContainer(AuthActivity.get_instance(self.sock))

        threading.Thread.__init__(self)
        print('Welcome')

    def run(self):
        while True:
            self.activity_container.run_activity()


if __name__ == '__main__':
    Client().start()
