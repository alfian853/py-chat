import sys
import socket
import select

def chat_client():
	if (len(sys.argv) < 3):
		print 'Sintaks : python namafile-python hostname port'
		sys.exit()
	
	host = sys.argv[1]
	port = int(sys.argv[2])
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(2)
	
	# connect to remote host
	try:
		s.connect((host, port))
	except:
		print 'Unable to connect'
		sys.exit()
	
	print 'Connected to remote host.'
	sys.stdout.write('[Me] ');
	sys.stdout.flush()
	
	while True:
		socket_list = [sys.stdin, s]
		
		# Get the list sockets which are readable
		ready_to_read, ready_to_write, in_error = select.select(socket_list, [], [])
		
		for sock in ready_to_read:
			if sock == s:
				# incoming message from remote server, s
				data = sock.recv(4096)
				if not data:
					print '\nDisconnected from chat server'
					sys.exit()
				else:
					# print data
					sys.stdout.write(data)
					sys.stdout.write('[Me] ');
					sys.stdout.flush()
			
			else:
				# user entered a message
				msg = sys.stdin.readline()
				s.send(msg)
				sys.stdout.write('[Me] ');
				sys.stdout.flush()


if __name__ == "__main__":
	sys.exit(chat_client())