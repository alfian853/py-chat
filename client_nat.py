import socket
import threading
import json

# dummy client Natasha
from env import Env


class Client(threading.Thread):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_addr = ('127.0.0.1', Env.server_port)
        self.sock.connect(server_addr)
        print('connected to '+str(server_addr))
        threading.Thread.__init__(self)

    def run(self):
        ClientReceiver(self.sock).start()
        while True:
            commands = input().split(' ')
            request = {}
            # request['COMMAND'] = 'AUTH-LOGIN'
            # request['username'] = 'alfian_liao'
            # request['password'] = 'mySecret'

            # request['COMMAND'] = 'AUTH-REGISTER'
            # request['username'] = 'alfian_liao2'
            # request['password'] = 'mySecret'
            # request['password-confirm'] = 'mySecret'

            request['COMMAND'] = commands[0]
            if request['COMMAND'] == 'AUTH-REGISTER' and commands[3]:
                request['username'] = commands[1]
                request['password'] = commands[2]
                request['password-confirm'] = commands[3]
            elif request['COMMAND'] == 'AUTH-LOGIN':
                request['username'] = commands[1]
                request['password'] = commands[2]
            elif request['COMMAND'] == 'AUTH-LOGOUT':
                request['token'] = commands[1]
            print (request)
            self.sock.sendall(json.dumps(request).encode('utf-8'))


class ClientReceiver(threading.Thread):
    def __init__(self, sock):
        self.sock = sock
        threading.Thread.__init__(self)

    def run(self):
        while True:
            response = self.sock.recv(1024)
            print(response.decode('utf-8'))


if __name__=="__main__":
    Client().start()

