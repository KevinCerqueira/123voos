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

import os
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import platform

# Classe para controlar a base de dados.
class DB:
	
	cluster = None
	
	database = None
	company = None
	airports = None
	routes = None
	
	# Construtor
	def __init__(self, company):
		self.cluster = MongoClient(self.env('CLUSTER'))
		self.company = company
		self.database = self.cluster[company]
		self.airports = self.database.airports
		self.routes = self.database.routes
			
	def env(self, var):
		env = '\\.env'
		if(platform.system() == 'Linux'):
			env = '/.env'
			
		with open(os.path.dirname(os.path.realpath(__file__)) + env, 'r', encoding='utf-8') as file_env:
			line = file_env.readline()
			while(line):
				content = line.split('=')
				if(content[0] == var):
					return content[1]
				line = file_env.readline()
	# Cria uma rota
	def createRoute(self, start, end, route):
		try:
			route = {
				'start': ObjectId(start),
				'end': ObjectId(end),
				'total_chairs': route['total_chairs'],
				'filled_chairs': route['filled_chairs'],
				'distance': route['distance'],
				'time': route['time'],
				'value': route['value']				
			}
			_id = self.routes.insert_one(route)
			return _id.inserted_id
		except:
			return None
	
	# Cria um aeroporto
	def createAirport(self, airport):
		try:
			_id = self.airports.insert_one(airport)			
			return _id.inserted_id
		except:
			return None
	
	# Encontra rotas a partir de uma key e value passada
	def findRoutes(self, key, value):
		try:
			if(key == '_id' or key == 'id'):
				key = '_id'
				value = ObjectId(value)
			elif(key == 'start' or key == 'end'):
				value = ObjectId(value)
			param = {key: value}
			if(key in ['_id']):
				return [self.routes.find_one(param)]
			else:
				routes = []
				for route in self.routes.find(param).sort('city', pymongo.ASCENDING):
					routes.append(route)
				return routes
		except:
			return None
	
	# Encontra rotas a partir de um objeto
	def getRoutes(self, param):
		try:
			routes = []
			for route in self.routes.find(param).sort('city', pymongo.ASCENDING):
				airport_start = self.getAirports({'_id': route['start']}) 
				airport_end = self.getAirports({'_id': route['end']}) 
				
				routes.append({
					'id': str(route['_id']), 
					'start': {
						'id': str(route['start']), 
						'name': airport_start[0]['name'], 
						'city': airport_start[0]['city'], 
						'uf': airport_start[0]['uf'], 
						'cep': airport_start[0]['cep']
					},
					'end': {
						'id': str(route['end']),
						'name': airport_end[0]['name'], 
						'city': airport_end[0]['city'], 
						'uf': airport_end[0]['uf'], 
						'cep': airport_end[0]['cep']
					},
					'total_chairs': route['total_chairs'], 
					'distance': route['distance'], 
					'filled_chairs': route['filled_chairs'], 
					'time': route['time'], 'value': route['value']
					})
			return routes
		except:
			return None
	
	# Encontra aeroportos a partir de uma key e value passada
	def findAirports(self, key, value):
		try:
			if(key == '_id' or key == 'id'):
				key = '_id'
				value = ObjectId(value)
			param = {key: value}
			if(key in ['_id']):
				return [self.airports.find_one(param)]
			else:
				airports = []
				for airport in self.airports.find(param).sort('city', pymongo.ASCENDING):
					airports.append(airport)
				return airports
		except:
			return None
	
	# Encontra aeroportos a partir de um objeto
	def getAirports(self, param):
		try:
			airports = []
			for airport in self.airports.find(param).sort('city', pymongo.ASCENDING):
				airports.append(airport)
			return airports
		except:
			return None
	
	# Atualiza uma rota
	def updateRoute(self, id, params):
		try:
			_id = ObjectId(id)
			self.routes.update_one({'_id': _id}, {'$set': params})
			return True
		except:
			return False
	
	# Confirma uma passagem
	def confirmTicket(self, route_id: str):
		try:
			route = self.findRoutes('id', route_id)[0]
			total_chairs = int(route['total_chairs'])
			filled_chairs = int(route['filled_chairs']) + 1
			if(filled_chairs > total_chairs):
				return False
			elif(self.updateRoute(route_id, {'filled_chairs': filled_chairs})):
				return True
			return False
		except:
			return False
	
	# Desconfirma uma passagem
	def disconfirmTicket(self, route_id: str):
		try:
			route = self.findRoutes('id', route_id)[0]
			filled_chairs = int(route['filled_chairs']) - 1
			if(filled_chairs == -1):
				return False
			elif(self.updateRoute(route_id, {'filled_chairs': filled_chairs})):
				return True
			return False
		except:
			return False