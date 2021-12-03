"""
 * Componente Curricular: MI Concorrência e Conectividade
 * Autor: Kevin Cerqueira Gomes e Esdras Abreu Silva
 *
 * Declaro que este código foi elaborado por mim de forma individual e
 * não contém nenhum trecho de código de outro colega ou de outro autor,
 * tais como provindos de livros e apostilas, e páginas ou documentos
 * eletrônicos da Internet. Qualquer trecho de código de outra autoria que
 * uma citação para o  não a minha está destacado com  autor e a fonte do
 * código, e estou ciente que estes trechos não serão considerados para fins
 * de avaliação. Alguns trechos do código podem coincidir com de outros
 * colegas pois estes foram discutidos em sessões tutorias.
"""
from db import DB
import socket
import json
import sys
import os
import threading
import base64
import re
import platform

from collections import deque

class Main:
	
	addr = None
	
	# Servidor
	server_socket = None
	
	# Controlador da base de dados
	db = None
	
	queue_request = None
	thread_request = None
	
	close = False
	
	def __init__(self, company):
		# Iniciando o Server
		self.db = DB(company)
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.addr = self.readAddress(company)
		self.server_socket.bind(self.addr)
		self.server_socket.listen(5)
		self.queue_request = deque()
		self.thread_request = threading.Thread(target=self.queueRequest)
		self.thread_request.start()
		print('SERVER {} ON AT {}:{}\n'.format(company, self.addr[0], self.addr[1]))
		self.work()
	
	def readAddress(self, company):
		addrs = '\\addr.txt'
		if(platform.system() == 'Linux'):
			addrs = '/addr.txt'
			
		with open(os.path.dirname(os.path.realpath(__file__)) + addrs, 'r', encoding='utf-8') as file_addrs:
			line = file_addrs.readline()
			while(line):
				content = line.split('=')
				if(content[0] == company):
					return (content[1].split(':')[0], int(content[1].split(':')[1]))
				line = file_addrs.readline()
		
	# Função principal, onde o servidor irá receber as conexões
	def work(self):
		while not self.close:
			client, address = self.server_socket.accept()
			print('ADDRESS: ', address)
			
			self.receptor(client)
		
		if(self.close and len(self.queue_request) == 0):
			print('SERVER OFF')
			self.server_socket.close()
			return sys.exit()
	
	# Trata os dados recebidos
	def receptor(self, client):
		path = ''
		data = None
		
		request_raw = client.recv(8192)
		
		request_clean = str(request_raw.decode('utf-8'))
		
		content_parts = request_clean.split(' ')
		path = content_parts[0].replace(' ', '')
		
		# Buscando por dados enviados na requisicao
		for index in request_clean:
			if(index == '{'):
				data = json.loads(request_clean[request_clean.find('{') :])

		# Adicionando a requisição a fila de requisições
		self.queue_request.append({'client': client, 'path': path, 'data': data})
	
	# Consome a fila de requisições
	def queueRequest(self):
		while not (self.close and len(self.queue_request) == 0):
			if(len(self.queue_request) > 0):
				print('conn: ' + str(len(self.queue_request)))
				request = self.queue_request.popleft()
				self.routing(request['client'], request['path'], request['data'])
		return 
	# Função responsável pelo roteamente, identifica os metodos e as rotas requisitadas
	def routing(self, client, path, data):

		print({'client': client, 'path': path, 'data': data})
		
		if(path == 'receive-routes'):
			pass
		elif(path == 'send-routes'):
			pass
		elif(path == 'confirm-route'):
			self.confirmRoute(client, data)
		elif(path == 'disconfirm-route'):
			self.disconfirmRoute(client, data)
		elif(path == 'graph'):
			pass
		elif(path == 'graph-general'):
			pass
		elif(path == 'close'):
			self.closeSocket(client)
		else:
			self.routeNotFound()
		return client.close()
	
	# Fecha a conexão do cliente
	def closeConnection(self, client):
		client.close()
	
	# Desliga o servidor
	def closeSocket(self, client):
		print('SERVIDOR FECHARA AO TERMINAR AS CONEXOES EXISTENTES')
		self.close = True
	
	# Caso a rota informada não esteja dentre as disponiveis
	def routeNotFound(self, client):
		return self.sendToClientError(client, 'Rota nao encontrada')
	
	# Envia dados para o cliente em caso de sucesso
	def sendToClientOk(self, client, obj):
		response = json.dumps({'success': True, 'data': obj})
		return client.sendall(bytes(response.encode('utf-8')))
	
	# Envia dados para o cliente em caso de erro
	def sendToClientError(self, client, msg):
		response = json.dumps({'success': False, 'error': msg})
		return client.sendall(bytes(response.encode('utf-8')))
	
	def confirmRoute(self, client, data):
		confirm = self.db.confirmTicket(data['route'])
		if confirm:
			return self.sendToClientOk(client, "Passagem confirmada com sucesso!")
		return self.sendToClientError(client, "Nao ha cadeiras mais disponiveis.")
	
	def disconfirmRoute(self, client, data):
		confirm = self.db.disconfirmTicket(data['route'])
		if confirm:
			return self.sendToClientOk(client, "Passagem desconfirmada com sucesso!")
		return self.sendToClientError(client, "Nao ha cadeiras nao disponiveis.")
				
if __name__ == '__main__':
	c = str(input('company: '))
	os.system("clear")
	m = Main(c)
	