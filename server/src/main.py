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
	
	# Endereços dos servidores cadastrados
	addr = None
	
	# Eu!
	me = ''
	
	# Servidores
	server_send = None
	server_receive = None
	
	# Controlador da base de dados
	db = None
	
	# Controle das requisições
	queue_request = None
	thread_request = None
	
	# Verifica se deve fechar o servidor
	close = False
	
	# Verifica quem quer ser o coordenador
	led = False
	leader  = ''
	
	# Controla quando quero ser coordenador
	ready_lead = False
	leading = False
	count_companies = 0
	
	def __init__(self, company):
		# Iniciando o Server
		self.me = company
		self.db = DB(company)
		self.server_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_receive = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.addr = self.readAddress(company)
		self.server_send.bind(self.addr)
		self.server_send.listen(5)
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
	
	def readAddressNot(self, not_company):
		addrs = '\\addr.txt'
		if(platform.system() == 'Linux'):
			addrs = '/addr.txt'
		companies = []
		with open(os.path.dirname(os.path.realpath(__file__)) + addrs, 'r', encoding='utf-8') as file_addrs:
			line = file_addrs.readline()
			while(line):
				content = line.split('=')
				if(content[0] != not_company):
					companies.append((content[1].split(':')[0], int(content[1].split(':')[1])))
				line = file_addrs.readline()
		return companies
		
	# Função principal, onde o servidor irá receber as conexões
	def work(self):
		while not self.close:
			client, address = self.server_send.accept()
			print('ADDRESS: ', address)
			
			self.receptor(client)
		
		if(self.close and len(self.queue_request) == 0):
			print('SERVER OFF')
			self.server_send.close()
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
		
		if(path == 'to-lead' and not self.ready_lead):
			# Adicionando pedido para liderar no começo da fila
			self.queue_request.appendleft({'client': client, 'path': path, 'data': data})
		elif(path == 'get-routes' and not self.led and self.leading):
			# Adicionando pedido dos liderados no começo da fila
			self.queue_request.appendleft({'client': client, 'path': path, 'data': data})	
		elif(not (path in ['get-routes', 'to-lead'])):
			# Adicionando a requisição no final da fila de requisições
			self.queue_request.append({'client': client, 'path': path, 'data': data})
		else:
			client.close()
	# Consome a fila de requisições
	def queueRequest(self):
		while not (self.close):
			if(len(self.queue_request) > 0 and not (self.ready_lead and not self.led)):
				print('conn: ' + str(len(self.queue_request)))
				request = self.queue_request.popleft()
				self.routing(request['client'], request['path'], request['data'])
			elif(self.ready_lead and not self.led):
				self.wantToLead()
		return sys.exit()
	# Função responsável pelo roteamente, identifica os metodos e as rotas requisitadas
	def routing(self, client, path, data):

		print({'client': client, 'path': path, 'data': data})
		
		if(path == 'to-lead'):
			self.electLeader(client, data)
		elif(path == 'get-routes'):
			self.sendRoutesToLed(client)
		elif(path == 'send-routes'):
			pass
		elif(path == 'confirm-route'):
			self.confirmRoute(client, data)
			self.ready_lead = True
		elif(path == 'disconfirm-route'):
			self.disconfirmRoute(client, data)
			self.ready_lead = True
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
	
	def electLeader(self, client, data):
		self.led = True
		print('{}:{} NOVO LIDER'.format(data['host'], data['port']))
		self.leader = (data['host'], data['port'])
		client.close()
		self.server_receive.connect(self.leader)
		self.server_receive.sendall(("get-routes ").encode('utf-8'))
		routes = self.server_receive.recv(8192)
		print(routes)
		self.server_receive.close()
		self.led = False
	
	def sendRoutesToLed(self, client):
		routes = self.db.getRoutes({})
		self.sendToClientOk(client, {'host': self.addr[0], 'port': self.addr[1], 'routes': routes})
		self.count_companies = self.count_companies - 1
		if(self.count_companies <= 0):
			self.leading = False
	
	def wantToLead(self):
		companies = self.readAddressNot(self.me)
		print(companies)
		self.count_companies = len(companies)
		self.leading = True
		for company in companies:
			print('CONECTANDO: {}:{}'.format(company[0], company[1]))
			try:
				self.server_receive.connect(company)
				self.server_receive.sendall(('to-lead {}'.format(json.dumps({'host': self.addr[0], 'port': self.addr[1]}))).encode('utf-8'))
				self.server_receive.close()
			except:
				self.count_companies = self.count_companies - 1
		self.ready_lead = False
	
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
	