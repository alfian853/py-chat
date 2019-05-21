import json
import socket
import threading


class Notifiable(object):

    def handle_notification(self, notification):
        pass


class Receiver(threading.Thread):

    def __init__(self, master: Notifiable, connection: socket.socket):
        super().__init__()
        self.conn = connection
        self.master = master
        self.is_running = True

    def stop(self):
        self.is_running = False

    def run(self):
        while self.is_running:
            notif = json.loads(self.conn.recv(1024).decode('utf-8'))
            self.master.handle_notification(notif)



