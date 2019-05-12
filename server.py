import json
import socket
import threading
import traceback

from handlers import AuthHandler
from handlers import CoreHandler
from session import Session
from env import Env

class Server(threading.Thread):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((Env.server_host, Env.server_port))
        print('Server on')
        threading.Thread.__init__(self)

    def run(self):
        self.sock.listen(1)
        while True:
            conn, address = self.sock.accept()
            print('new client > ' + str(address))

            broker = RequestBroker(conn, address)
            broker.push_back_handler(AuthHandler.get_instance())
            broker.push_back_handler(CoreHandler.get_instance())
            broker.start()


class RequestBroker(threading.Thread):

    def __init__(self, connection, address):
        threading.Thread.__init__(self)
        self.connection = connection
        self.address = address
        self.handler_head = None
        self.handler_tail = None

    def push_back_handler(self, handler):
        if self.handler_head is None:
            self.handler_head = handler
            self.handler_tail = handler
        else:
            self.handler_tail.set_next_handler(handler)
            self.handler_tail = handler

    def run(self):
        Session.set_connection(self.connection)
        while True:
            try:
                data = self.connection.recv(1024)
                request = json.loads(data.decode('utf-8'))
                print(request)
                if self.handler_head is not None:
                    self.handler_head.handle(request)

            except Exception as e:
                traceback.print_exception(e)
                Session.send_response({
                    'status': 'failed',
                    'message': 'internal server error'
                })


if __name__ == "__main__":
    Server().start()
