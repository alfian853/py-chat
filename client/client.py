import socket
import threading
import json


# dummy client,
from env import Env


class Client(threading.Thread):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_addr = ('127.0.0.1', Env.server_port)
        self.sock.connect(server_addr)
        print('connected to '+str(server_addr))
        threading.Thread.__init__(self)
        print('Welcome, do you have account?')
        print('NO: Please type "AUTH-REGISTER yourname yourpass repeatpass" without quotation marks')
        print('YES: Please type "AUTH-LOGIN yourname yourpass" without quotation marks')

    def run(self):
        ClientReceiver(self.sock).start()
        while True:
            commands = input().split(' ')
            request = {}
            
            if(commands[0] == "AUTH-REGISTER"):
                request['COMMAND'] = commands[0]
                request['username'] = commands[1]
                request['password'] = commands[2]
                request['password-confirm'] = commands[3]
            elif(commands[0] == "AUTH-LOGIN"):
                request['COMMAND'] = commands[0]
                request['username'] = commands[1]
                request['password'] = commands[2]
            elif(commands[0] == "AUTH-LOGOUT"):
                # request['token'] = Session.token()
                request['COMMAND'] = commands[0]
            else:
                request['COMMAND'] = commands[0]
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

