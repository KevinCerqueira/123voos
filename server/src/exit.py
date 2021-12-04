import socket
import json
import sys
import time

HOST = 'localhost'
PORT = 8000


rota = 'close'

request = '{} '.format(rota)
for i in [1,2,3]:
	client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	client1.connect((HOST, 8200))
	client2.connect((HOST, 8100))
	client3.connect((HOST, 8000))

	client1.sendall((request).encode('utf-8'))
	client2.sendall((request).encode('utf-8'))
	client3.sendall((request).encode('utf-8'))

	client1.close()
	client2.close()
	client3.close()

sys.exit()