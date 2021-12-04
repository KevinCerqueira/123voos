import socket
import json
import sys
import time

HOST = 'localhost'
PORT = 8100

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
# input()
# send = input()
# send = {'id': 1, 'nome': 'Kevin', 'saturacao': 87, 'batimento': 98, 'pressao': 97}
# send = {'id': 2, 'saturacao': 999, 'batimento': 999, 'pressao': 999, 'temperatura': 999}
# send = {'username': 'kevinprincipal', 'password': '123'}
# send = {'id': '0', 'value': 89}
# send = {'nome': 'Paciente'+str(i), 'idade': 70 - 10}
send = {'route': '61a819d5ce82b2941ebd8352'}
# send = {'id': 0}
# send = {}
# client.sendall(str.encode('Kevin'))
# metodo = 'POST'
# rota = '/get/patient/0'
# rota = '/update/patient'
# rota = '/register/patient'
rota = 'confirm-route'
# rota = 'close'
# rota = '/delete/patient'
# host = HOST+':'+str(PORT)
# auth = 'Authorization: Bearer a2V2aW4yOjEyMw=='
# auth = ''
# request = '{} {} HTTP/1.1\r\nHost: {}\r\nUser-Agent: client\r\nContent-Type: application/json\r\n{}\r\nAccept: */*\r\nContent-Length: 21\r\n\r\n{}'.format(metodo, rota, host, auth, json.dumps(send))
request = '{} {}'.format(rota, json.dumps(send))

# print(request)
# client.sendall('--method:POST --path:/register/patient --data:{}'.format(json.dumps(send)).encode('utf-8'))
# client.sendall('POST /register/doctor {}'.format(json.dumps(send)).encode('utf-8'))
# client.sendall('POST /register/patient HTTP/1.1 {}'.format(json.dumps(send)).encode('utf-8'))
# client.sendall(metodo + b' ' + rota + b' HTTP/1.1\r\nHost: ' + host + b'\r\nUser-Agent: client\r\nContent-Type: application/json\r\n' + auth + b'\r\nAccept: */*\r\nContent-Length: 21\r\n\r\n'+ json.dumps(send))
client.sendall((request).encode('utf-8'))
data = client.recv(8192)
print('Msg', data.decode())
# time.sleep(1)

# fecha = int(input('Fecha?'))
# if(fecha == 1):
# 	metodo = 'GET'
# 	rota = '/close-socket'
# 	request = '{} {} HTTP/1.1\r\nHost: {}\r\nUser-Agent: client\r\nContent-Type: application/json\r\n{}\r\nAccept: */*\r\nContent-Length: 21\r\n\r\n{}'.format(metodo, rota, host, auth, json.dumps(send))
# 	client.sendall((request).encode('utf-8'))
	
client.close()
sys.exit()