import json
import socket

# session storage
import entities
from entities import UserEntity


class SessionManager:
    session_list = []

    @staticmethod
    def get_by_username(username):
        print(SessionManager.session_list)
        for session in SessionManager.session_list:
            print(session.user.username)
            if session.user.username == username:
                return session
        return None

    @staticmethod
    def add_to_list(session):
        SessionManager.session_list.append(session)

    @staticmethod
    def del_from_list(session):
        SessionManager.session_list.remove(session)

class Session:
    connection: socket.socket
    user: UserEntity

    # threading.local() agar datanya dipisah untuk setiap thread
    # storage = threading.local()

    def __init__(self):
        self.connection = None
        self.user = None
        self.token = None

    def set_connection(self, connection: socket.socket):
        self.connection = connection

    # pakai ini untuk add ke session manager
    def set_login_user(self, user: entities.UserEntity):
        self.user = user
        SessionManager.add_to_list(self)

    def send_response(self, response):
        print('send > ')
        print(response)
        if isinstance(response, dict):
            self.connection.sendall(json.dumps(response).encode('utf-8'))
        else:
            self.connection.sendall(response.encode('utf-8'))

    # hapus data login
    def clear(self):
        self.user = None
        self.token = None


