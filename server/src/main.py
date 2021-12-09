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
import platform
import time
import random

from collections import deque

class Main:
	
	starting = False
	
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
	
	# Verifica quem quer ser o lider
	led = False
	leader  = None
	
	# Controla quando quero ser lider
	ready_send = False # Pronto para enviar
	ready_lead = False # Pronto para liderar
	leading = False # Liderando
	# Quantidade de servidores que vou receber as requisições quando me tornar líder
	count_companies = 0
	
	all_routes = None
	
	def __init__(self, company):
		# Iniciando o Server
		self.me = company
		print('INICIANDO SERVIDOR, POR FAVOR AGUARDE...')
		
		print('CONECTANDO AO BANCO DE DADOS...')
		self.db = DB(company)
		self.server_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		print('LENDO ALGUNS ARQUIVOS...')
		self.addr = self.readAddress(company)
		start = self.readCtrl()
		os.system('clear')
		if(not start):
			self.ready_lead = True
			time.sleep(4)
			self.wantToLead()
		
		print('ABRINDO PORTAS DO SERVIDOR... {}:{}'.format(self.addr[0], self.addr[1]))
		self.server_send.bind(self.addr)
		self.server_send.listen(5)
		
		print('SERVIDOR PRONTO PARA INICAR...')
		
		print('INICIANDO...')
		self.queue_request = deque()
		self.thread_request = threading.Thread(target=self.queueRequest)
		self.thread_request.start()
		self.queue_response = deque()
		self.thread_response = threading.Thread(target=self.queueResponse)
		self.thread_response.start()
			
		print('SERVER {} ON AT {}:{}\n'.format(company, self.addr[0], self.addr[1]))
		
		self.work()
	
	# Ler o arquivo com os endereços dos servidores
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
	
	# Ler o arquivo de controle
	def readCtrl(self):
		ctrl = '\\.ctrl'
		if(platform.system() == 'Linux'):
			ctrl = '/.ctrl'
		
		start = True
		with open(os.path.dirname(os.path.realpath(__file__)) + ctrl, 'r', encoding='utf-8') as file_ctrl:
			line = file_ctrl.readline()
			if(line == 'false'):
				start = False
		
		if(not start):			
			with open(os.path.dirname(os.path.realpath(__file__)) + ctrl, 'w', encoding='utf-8') as file_ctrl:
				line = file_ctrl.write('true')
		return start
	
	# Ler todos os endereços de todos os servidores exceto o passado por parametro		
	def readAddressNot(self, not_company):
		addrs = '\\addr.txt'
		if(platform.system() == 'Linux'):
			addrs = '/addr.txt'
		companies = []
		with open(os.path.dirname(os.path.realpath(__file__)) + addrs, 'r', encoding='utf-8') as file_addrs:
			line = file_addrs.readline()
			while(line):
				content = line.split('=')
				if(content[0] != not_company and content[0] != 'default'):
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
		request_raw = client.recv(8192)
		
		path, data = self.cleanRequest(request_raw)
		
		if(path == 'to-lead' and not self.led):
			# Adicionando pedido para liderar no começo da fila
			self.queue_response.appendleft({'client': client, 'path': path, 'data': data})
		elif(path == 'get-routes' and ((not self.led and self.leading) or self.starting)):
			# Adicionando pedido dos liderados no começo da fila
			self.queue_response.appendleft({'client': client, 'path': path, 'data': data})	
		elif(not (path in ['get-routes', 'to-lead'])):
			# Adicionando a requisição no final da fila de requisições
			self.queue_request.append({'client': client, 'path': path, 'data': data})
		elif(path == 'to-lead'):
			self.queue_request.append({'client': client, 'path': path, 'data': data})
		else:
			self.sendToClientError(client, 'Acho que estamos com alguns problemas...')

	# Limpa a requisição
	def cleanRequest(self, request_raw):
		path = ''
		data = None
		request_clean = str(request_raw.decode('utf-8'))
		content_parts = request_clean.split(' ')
		path = content_parts[0].replace(' ', '')
		
		# Buscando por dados enviados na requisicao
		for index in request_clean:
			if(index == '{'):
				data = json.loads(request_clean[request_clean.find('{') :])
		
		return (path, data)

	# Consome a fila de requisições
	def queueRequest(self):
		while not (self.close):
			if(len(self.queue_request) > 0 and not (self.ready_lead and not self.led)):
				request = self.queue_request.popleft()
				self.routing(request['client'], request['path'], request['data'])
			elif(self.ready_lead and not self.led):
				self.wantToLead()
		return sys.exit()
	
	# Consome a fila de requisições
	def queueResponse(self):
		while not (self.close):
			if(len(self.queue_response) > 0):
				request = self.queue_response.popleft()
				self.routing(request['client'], request['path'], request['data'])
		return sys.exit()
		
	# Função responsável pelo roteamente, identifica os metodos e as rotas requisitadas
	def routing(self, client, path, data):
		
		if(path == 'to-lead'):
			self.electLeader(client, data)
		elif(path == 'get-routes'):
			self.sendRoutesToLed(client)
		elif(path == 'who-leader'):
			if(self.leading):
				self.sendToClientOk(client, {'host': self.addr[0], 'port': self.addr[1]})
			elif(self.leader != None):
				self.sendToClientOk(client, {'host': self.leader[0], 'port': self.leader[1]})
			else:
				self.sendToClientOk(client, {'host': self.addr[0], 'port': self.addr[1]})
				
		elif(path == 'get-all-routes'):
			self.getAllRoutes(client)
		elif(path == 'confirm-route'):
			self.confirmRoute(client, data)
		elif(path == 'disconfirm-route'):
			self.disconfirmRoute(client, data)
		elif(path == 'get-route'):
			self.findRoute(client, data)
		elif(path == 'close'):
			self.closeSocket()
		else:
			self.routeNotFound(client)
		return client.close()
	
	# Desliga o servidor
	def closeSocket(self):
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
	
	# Eleger líder
	def electLeader(self, client, data):
		self.led = True
		print('{}:{} NOVO LIDER'.format(data['host'], data['port']))
		self.leader = (data['host'], data['port'])
		myroutes = self.db.getRoutes({})
		print(myroutes)
		self.sendToClientOk(client, {'company': self.me, 'host': self.addr[0], 'port': self.addr[1], 'routes': myroutes})
		client.close()
		time.sleep(5)
		success = False
		count = 0
		while(not success and count <= 10):
			try:
				leader_receive = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				leader_receive.connect(self.leader)
				leader_receive.sendall(("get-routes ").encode('utf-8'))
				response = leader_receive.recv(8192)
				path, data = self.cleanRequest(response)
				self.starting = False
				self.all_routes = {'company': self.me, 'host': self.addr[0], 'port': self.addr[1], 'companies': None}
				companies = []
				companies.append({'company': self.me, 'host': self.addr[0], 'port': self.addr[1], 'routes': myroutes})
				companies.append(data['data']['routes'])
				self.all_routes['companies'] = companies
				leader_receive.close()
				success = True
			except:
				count = count + 1
				success = False
				time.sleep(2)
		self.led = False
	
	# Enviado as rotas para os liderados
	def sendRoutesToLed(self, client):
		self.starting = False
		self.sendToClientOk(client, {'company': self.me, 'host': self.addr[0], 'port': self.addr[1], 'routes': self.db.getRoutes({})})
		self.count_companies = self.count_companies - 1
		if(self.count_companies <= 0):
			self.leading = False
	
	# Quero ser líder!
	def wantToLead(self):
		if not self.led:
			companies_addrs = self.readAddressNot(self.me)
			self.count_companies = len(companies_addrs)
			self.leading = True
			self.leader = (self.addr[0], self.addr[1])
			
			self.all_routes = {'company': self.me, 'host': self.addr[0], 'port': self.addr[1], 'companies': None}
			companies = []
			companies.append({'company': self.me, 'host': self.addr[0], 'port': self.addr[1], 'routes': self.db.getRoutes({})})

			for company in companies_addrs:
				print('-----------------')
				print('CONECTANDO: {}:{}'.format(company[0], company[1]))
				
				try:
					led_receive = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					led_receive.connect(company)
					led_receive.sendall(('to-lead {}'.format(json.dumps({'host': self.addr[0], 'port': self.addr[1]}))).encode('utf-8'))
					response = led_receive.recv(8192)
					path, data = self.cleanRequest(response)
					companies.append({'company': data['data']['company'], 'host': data['data']['host'], 'port': data['data']['port'], 'routes': data['data']['routes']})
					# companies.append(data['data']['routes'])
					led_receive.close()
				except Exception as e:
					print('Impossivel de enviar requerimento: {}'.format(e))
					self.count_companies = self.count_companies - 1
			
			self.all_routes['companies'] = companies	
			print(self.all_routes)
			print('-----------------')
			self.ready_send = True
			self.ready_lead = False
			
	
	# Confirmando rota
	def confirmRoute(self, client, data):
		confirm = self.db.confirmTicket(data['route'])
		if confirm:
			self.ready_lead = True
			return self.sendToClientOk(client, "Passagem confirmada com sucesso!")
		return self.sendToClientError(client, "Nao ha cadeiras mais disponiveis.")
	
	# Desconfirmando rota
	def disconfirmRoute(self, client, data):
		disconfirm = self.db.disconfirmTicket(data['route'])
		if disconfirm:
			self.ready_lead = True
			return self.sendToClientOk(client, "Passagem desconfirmada com sucesso!")
		return self.sendToClientError(client, "Nao ha cadeiras nao disponiveis.")
	
	# Pegar todas as rotas
	def getAllRoutes(self, client):
		if(self.all_routes == None):
			self.all_routes = {'company': self.me, 'host': self.addr[0], 'port': self.addr[1], 'companies': None}
			companies = []
			companies.append({'company': self.me, 'host': self.addr[0], 'port': self.addr[1], 'routes': self.db.getRoutes({})})
		return self.sendToClientOk(client, self.all_routes)
		
	def findRoute(self, client, data):
		route = self.db.findRoutes(data['type'], data['id'])
		if(route != None):
			return self.sendToClientOk(client, route)
		return self.sendToClientError('Rota nao encontrada')
				
if __name__ == '__main__':
	c = str(input('company: '))
	os.system("clear")
	m = Main(c)
	