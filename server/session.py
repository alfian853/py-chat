import json
import threading
import socket

# session storage
import entities


class Session:
    # threading.local() agar datanya dipisah untuk setiap thread
    storage = threading.local()

    @staticmethod
    def connection() -> socket.socket:
        return Session.storage.connection

    @staticmethod
    def set_connection(connection: socket.socket):
        Session.storage.connection = connection

    @staticmethod
    def user() -> entities.UserEntity:
        return Session.storage.user

    @staticmethod
    def set_user(user: entities.UserEntity):
        Session.storage.user = user

    @staticmethod
    def token():
        return Session.storage.token

    @staticmethod
    def set_token(token):
        Session.storage.token = token

    @staticmethod
    def send_response(response):
        print('send > ')
        print(response)
        if isinstance(response, dict):
            Session.connection().sendall(json.dumps(response).encode('utf-8'))
        else:
            Session.connection().sendall(response.encode('utf-8'))

    # hapus data login
    @staticmethod
    def clear():
        Session.storage.user = None
        Session.storage.token = None
