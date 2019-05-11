import json
import socket
import threading

from handlers import AuthHandler
from handlers import CoreHandler


class Server(threading.Thread):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('127.0.0.1', 10002))
        print('Server on')
        threading.Thread.__init__(self)

    def run(self):
        self.sock.listen(1)
        while True:
            conn, address = self.sock.accept()
            print('new client > ' + str(address))

            broker = RequestBroker(conn, address)
            broker.push_back_handler(AuthHandler())
            broker.push_back_handler(CoreHandler())
            broker.start()


class RequestBroker(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        self.handler_head = None
        self.handler_tail = None
        threading.Thread.__init__(self)

    def push_back_handler(self, handler):
        if self.handler_head is None:
            self.handler_head = handler
            self.handler_tail = handler
        else :
            self.handler_tail.set_next_handler(handler)
            self.handler_tail = handler

    def run(self):
        while True:
            data = self.connection.recv(1024)
            request = json.loads(data)
            if self.handler_head is not None:
                self.handler_head.handle(request)


if __name__ == "__main__":
    Server().start()
