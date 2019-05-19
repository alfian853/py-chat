import socket
import threading
import json

# dummy client Natasha
from env import Env

client_token = ''

class Client(threading.Thread):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_addr = ('127.0.0.1', Env.server_port)
        self.sock.connect(server_addr)
        print('connected to '+str(server_addr))
        threading.Thread.__init__(self)

    def run(self):
        # request = {}
        ClientReceiver(self.sock).start()
        while True:
            commands = input().split(' ')
            request = {}
            global client_token

            # request['COMMAND'] = 'AUTH-LOGIN'
            # request['username'] = 'alfian_liao'
            # request['password'] = 'mySecret'

            # request['COMMAND'] = 'AUTH-REGISTER'
            # request['username'] = 'alfian_liao2'
            # request['password'] = 'mySecret'
            # request['password-confirm'] = 'mySecret'

            if client_token:
                request['token'] = client_token

            request['COMMAND'] = commands[0]
            if request['COMMAND'] == 'AUTH-REGISTER' and commands[3]:
                request['username'] = commands[1]
                request['password'] = commands[2]
                request['password-confirm'] = commands[3]
            elif request['COMMAND'] == 'AUTH-LOGIN':
                request['username'] = commands[1]
                request['password'] = commands[2]
            elif request['COMMAND'] == 'AUTH-LOGOUT':
                client_token = ''

            print (request)
            self.sock.sendall(json.dumps(request).encode('utf-8'))


class ClientReceiver(threading.Thread):
    def __init__(self, sock):
        self.sock = sock
        threading.Thread.__init__(self)

    def run(self):
        while True:
            response = self.sock.recv(1024)
            # print ('===========================')
            # print(response.decode('utf-8'))
            jsonResponse = json.loads(response.decode('utf-8'))
            # print(jsonResponse)
            global client_token
            if jsonResponse['token']:
                client_token = jsonResponse['token']
            # print ('===========================')


if __name__=="__main__":
    Client().start()

