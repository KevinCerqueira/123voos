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
from posixpath import expanduser
import sys
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import platform
import networkx as nx
import matplotlib.pyplot as plt

# Classe para controlar a base de dados.
class DB:
	
	cluster = None
	
	database = None
	company = None
	airports = None
	routes = None
	
	graph = None
	
	# Construtor
	def __init__(self, company):
		self.cluster = MongoClient(self.env('CLUSTER'))
		self.company = company
		self.database = self.cluster[company]
		self.airports = self.database.airports
		self.routes = self.database.routes
		self.graph = nx.Graph()
			
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
		
	def createAirport(self, airport):
		try:
			_id = self.airports.insert_one(airport)			
			return _id.inserted_id
		except:
			return None
	
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
	
	def getRoutes(self, param):
		try:
			routes = []
			for route in self.routes.find(param).sort('city', pymongo.ASCENDING):
				routes.append({'id': str(route['_id']), 'start': str(route['start']), 'end': str(route['end']), 'total_chairs': route['total_chairs'], 'distance': route['distance'], 'filled_chairs': route['filled_chairs'], 'time': route['time'], 'value': route['value']})
			return routes
		except:
			return None
	
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
	
	def getAirports(self, param):
		try:
			airports = []
			for airport in self.airports.find(param).sort('city', pymongo.ASCENDING):
				airports.append(airport)
			return airports
		except:
			return None
	
	def updateRoute(self, id, params):
		try:
			_id = ObjectId(id)
			self.routes.update_one({'_id': _id}, {'$set': params})
			return True
		except:
			return False
	
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
			
			
	def mountInternalGraph(self):
		routes = self.getRoutes({})
		airports = self.getAirports({})
		for airport in airports:
			node = airport['city'] + '_' + airport['cep']
			self.graph.add_node(node)
			
		for route in routes:
			start = self.getAirports({'_id': ObjectId(route['start'])})
			end = self.getAirports({'_id': ObjectId(route['end'])})
			start_id = start[0]['city'] + '_' + start[0]['cep']
			end_id = end[0]['city'] + '_' + end[0]['cep']
			self.graph.add_edge(start_id, end_id)
			self.graph[start_id][end_id]['total_chairs'] = route['total_chairs']
			self.graph[start_id][end_id]['filled_chairs'] = route['filled_chairs']
			self.graph[start_id][end_id]['distance'] = route['distance']
			self.graph[start_id][end_id]['time'] = route['time']
			self.graph[start_id][end_id]['value'] = route['value']
			
		return self.graph
			
# if __name__ == "__main__":
# 	db = DB('anil')
	# air1 = db.createAirport({'city': 'Belo Horizonte', 'name': 'Aeroporto de BH', 'uf': 'MG' ,'cep': '98797888'})
	# air2 = db.createAirport({'city': 'Belém', 'name': 'Aeroporto de Belém', 'uf': 'PA' ,'cep': '79955789'})
	# route = db.createRoute(air1, air2, {'total_chairs': 40, 'filled_chairs': 1, 'distance': 600, 'time': 60, 'value': 349.99})
	# print(db.findAirports('cep', '41510045'))
	# G = nx.petersen_graph()
	# subax1 = plt.subplot(121)
	# print (db.createRoute('61a83a0a6c63cdb68f866d77', '61a81fa1a3400dd9e312245e', {'total_chairs': 40, 'filled_chairs': 1, 'distance': 600, 'time': 60, 'value': 349.99}))
	''''''
	# G = db.mountInternalGraph()	
	# pos = nx.spring_layout(G)
	# edge_labels = nx.get_edge_attributes(G, 'value')
	# nx.draw_networkx_edge_labels(G, pos, edge_labels)
	# nx.draw_networkx(G)
	# plt.show()
	''''''
	# print(db.confirmTicket('61a819d5ce82b2941ebd8352'))
	# nx.draw(G, with_labels=True, font_weight='bold')
	# nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
	# nx.draw(G, with_labels=True)
	# subax2 = plt.subplot(122)
	# db.mountInternalGraph()