import socket
import json
import sys
import time

HOST = 'localhost'
PORT = 8000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

rota = 'close'

request = '{} '.format(rota)

client.sendall((request).encode('utf-8'))
data = client.recv(8192)
print('Msg', data.decode())
client.close()

client.connect((HOST, PORT))
client.sendall((request).encode('utf-8'))
data = client.recv(8192)
print('Msg', data.decode())
	
client.close()
sys.exit()