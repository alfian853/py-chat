import asyncore
import json
import socket
import threading
import traceback

from env import Env
from handlers import AuthHandler
from handlers import CoreHandler
from session import Session, SessionManager


class Server(asyncore.dispatcher):
    def __init__(self):
        super().__init__()
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((Env.server_host, Env.server_port))
        self.listen(5)
        print('Server on')

    def handle_accept(self):
        conn, address = self.accept()
        print('new client > ' + str(address))

        broker = RequestBroker(conn, address)
        broker.push_back_handler(AuthHandler.get_instance())
        broker.push_back_handler(CoreHandler.get_instance())
        broker.start()


class RequestBroker(threading.Thread):

    def __init__(self, connection: socket.socket, address):
        super().__init__()
        self.connection = connection
        self.address = address
        self.handler_head = None
        self.handler_tail = None
        self.session = Session()
        self.session.set_connection(self.connection)

    def push_back_handler(self, handler):
        if self.handler_head is None:
            self.handler_head = handler
            self.handler_tail = handler
        else:
            self.handler_tail.set_next_handler(handler)
            self.handler_tail = handler

    def run(self):
        while True:
            try:
                data = self.connection.recv(1024)
                request = json.loads(data.decode('utf-8'))
                print(request)
                if self.handler_head is not None:
                    self.handler_head.handle(self.session, request)
            except BaseException as e:
                traceback.print_exc()
                try:
                    self.session.send_response({
                        'FOR': None,
                        'status': 'failed',
                        'message': 'internal server error'
                    })
                except:
                    # unregis jika client terputus
                    SessionManager.del_from_list(self.session)
                    self.connection.close()
                    return

# class RequestBroker(asyncore.dispatcher_with_send):
#
#     def __init__(self, connection, address):
#         super().__init__(connection)
#         self.connection = connection
#         self.address = address
#         self.handler_head = None
#         self.handler_tail = None
#         self.session = Session()
#         self.session.set_connection(self.connection)
#
#     def push_back_handler(self, handler):
#         if self.handler_head is None:
#             self.handler_head = handler
#             self.handler_tail = handler
#         else:
#             self.handler_tail.set_next_handler(handler)
#             self.handler_tail = handler
#
#     def handle_read(self):
#         data = self.connection.recv(1024)
#         request = json.loads(data.decode('utf-8'))
#         print(request)
#         try:
#             if self.handler_head is not None:
#                 self.handler_head.handle(self.session, request)
#         except BaseException as e:
#             traceback.print_exc()
#             raise e
#
#     def handle_error(self):
#         try:
#             self.session.send_response({
#                 'FOR': None,
#                 'status': 'failed',
#                 'message': 'internal server error'
#             })
#         except:
#             SessionManager.del_from_list(self.session)
#             self.close()
#

if __name__ == "__main__":
    Server()
    asyncore.loop()
