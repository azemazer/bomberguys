# -*- coding: utf-8 -*-
#                           ██╗██████╗ ██╗           
#                           ██║╚════██╗██║           
#                           ██║ █████╔╝██║           
#                      ██   ██║██╔═══╝ ██║           
#                      ╚█████╔╝███████╗███████╗      
#                       ╚════╝ ╚══════╝╚══════╝      
#                       https://jusdeliens.com
#
# Designed with 💖 by Jusdeliens
# Under CC BY-NC-ND 3.0 licence 
# https://creativecommons.org/licenses/by-nc-nd/3.0/ 

# Allow import without error 
# "relative import with no known parent package"
# In vscode, add .env file with PYTHONPATH="..." 
# with the same dir to allow intellisense
import sys
import os
__workdir__ = os.path.dirname(os.path.abspath(__file__))
__libdir__ = os.path.dirname(__workdir__)
sys.path.append(__libdir__)

os.system("export LANG=en_US.UTF-8")

import paho.mqtt.client as mqtt
import time
import json
import threading # or from concurrent.futures import thread
import copy
import codecs
import traceback
from datetime import datetime 

import pyanalytx.logger as anx
from pyludx.player import *
from pyludx.robot import *

class IArena:
	def start(self):
		...
	def stop(self):
		...
	def reset(self):
		...
	def update(self):
		...
	def addPlayer(self, robotId:str, isPnj:bool) -> IPlayerModel:
		...
	def _onRobotAdded(self,robotId:str, rules:dict[str,Any], players:dict[str,IPlayerModel], robots:dict[str,IRobotModel]) -> IRobotModel:
		"""
		To be overriden to do something here after the robot is added to the arena
		Must return the instance of the new robot to add into the arena
		"""
		...
	def _onRobotRemoved(self,robot:IRobotModel) -> None:
		"""
		To be overriden to do something after the robot is popped from arena
		"""
		...
	def _onPlayerAdded(self, clientId:str, playerId:str, robotId:str, rules:dict[str,Any], players:dict[str,IPlayerModel], robots:dict[str,IRobotModel]) -> IPlayerModel:
		"""
		To be overriden to do something here after the player is added to the arena
		Must return the instance of the new player to add into the arena
		"""
		...
	def _onPlayerRemoved(self,player:IPlayerModel) -> None:
		"""
		To be overriden to do something after the player is popped from arena
		"""
		...
	def _onReset(self, rules:dict[str,Any]) -> None:
		"""To be overriden"""
		...
	def _onUpdate(self, rules:dict[str,Any], players:dict[str,IPlayerModel], robots:dict[str,IRobotModel]) -> None:
		"""To be overriden"""
		...
	def _onPlayerUpdate(self, player:IPlayerModel, rules:dict[str,Any], players:dict[str,IPlayerModel], robots:dict[str,IRobotModel]) -> None:
		"""To be overriden"""
		...
	def _onRequestRx(self, key:str, value:Any):
		...

	def updateRequest(self, req:dict[str,Any]) -> int:
		"""
		Returns the number of requests performed
		To be overriden
		"""
		...

class Arena(IArena):       
	"""
	Main class to be the engine of an arena
	Can be inheriten and its methods overriden to add functionalities
	"""
	topicRobotsState = "robotx/clients/state"
	topicRobotsRequest = "robotx/clients/request"
	topicPlayersState = "ludx/clients/state"
	topicPlayersRequest = "ludx/clients/request"
	topicServerState = "ludx/server/state"
	topicServerRequest = "ludx/server/request"
	topicServerPing = "ludx/server/ping"
	rules = {
		# 🛠️ Règles pour créer l'instance de l'arène
        "verbosity": { "?fr":"", "ini":3, "readonly":True, "publish":False },
        "logDir": { "?fr":"", "ini":".log", "readonly":True, "publish":False },
        "arenaName" : { "?fr":"", "ini":"beta", "readonly":True, "publish":False },
        "restartOnExcept": { "?fr":"", "ini":False, "readonly":True, "publish":False },
        "factoryDir" : { "?fr":"", "ini":"pytactx_arena", "readonly":True, "publish":False },
        "factoryFile" : { "?fr":"", "ini":"arena", "readonly":True, "publish":False },
        "factoryClass" : { "?fr":"", "ini":"Arena", "readonly":True, "publish":False },
        "username" : { "?fr":"", "ini":"server", "readonly":True, "publish":False },
        "password" : { "?fr":"", "ini":"serverrulestheworld", "readonly":True, "publish":False },
        "brokerAddress": { "?fr":"", "ini":"mqtt.jusdeliens.com", "readonly":True, "publish":False },
        "brokerPort": { "?fr":"", "ini":1883 },
		"desc" : { "?fr":"Description de l'arene", "ini":"Arène d'initiation au développement Python", "publish":True },

		# 🖼️ Règle pour customiser le viewer de l'arène : taille, images, couleurs ...
        "gridColumns" : { "?fr":"Nombre de colonnes dans la grille", "ini":40, "min":0, "max":50, "publish":True },
        "gridRows" : { "?fr":"Nombre de lignes dans la grille", "ini":30, "min":0, "max":50, "publish":True },
        "resPath" : { "?fr":"Adresse vers le serveur des resources images", "ini":"https://jusdeliens.com/play/pytactx/resources/", "publish":True },
        "bgImg" : { "?fr":"Url de l image de fond", "ini":"gta5.jpg", "publish":True },
        "logo" : { "?fr":"Url du logo de l arene", "ini":"j2l.png", "publish":True },
        "bgColor" : { "?fr":"Code rgba du fond de l arene", "ini":[255,255,255,0.4], "publish":False },
        "gridColor" : { "?fr":"Code rgba des lignes et colonnes de l arene", "ini":[255,255,255,0.4], "publish":True },
		"viewer" : { "?fr":"Nom du viewer par défaut pour afficher l'arene", "ini":"pytactx", "publish":True },
		"api" : { "?fr":"URL vers api", "ini":"https://replit.com/@jusdeliens", "publish":True },
		"help" : { "?fr":"URL vers tutos", "ini":"https://tutos.jusdeliens.com", "publish":True },

		# 🚷 Règles pour gérer les joueurs
		"nPlayers" : { "?fr":"Le nombre actuel de players", "ini":0, "min":0, "max":100, "readonly":True, "publish":True },
		"nRobots" : { "?fr":"Le nombre actuel de robots physiques", "ini":0, "min":0, "max":100, "readonly":True, "publish":True },
		"maxPlayers" : { "?fr":"Nombre max de players autorisés", "ini":20, "min":0, "max":100, "reset":True, "publish":True },
		"onlyAuthorised" : { "?fr":"Filtrer les noms des players", "ini":False, "reset":True, "publish":True },
		"authorised" : { "?fr":"Filtrer les noms des players", "ini":{}, "publish":True},
		"nameLen" : { "?fr":"Longueur de nom max", "ini":32, "min":1, "max":100, "publish":False },
		"maxRobots" : { "?fr":"Nombre de robots sur l'écran", "ini":8, "min":1, "max":100, "publish":True },

		# 💾 Règles pour sauvegarder les scripts des joueurs
        "saveSrc" : { "?fr":"Active sauvegarde des sources envoyees par les joueurs", "ini":True, "publish":False },
        "srcExts" : { "?fr":"Extensions authorises pour save", "ini":[".py"], "publish":True },        
        "saveSrcDir" : { "?fr":"Sauvegarde des sources avec subdirs", "ini":True, "publish":False },        
        "saveNb" : { "?fr":"Nb max de sauvegardes de versions des sources envoyees par les joueurs authorises", "ini":10, "publish":True },        

		# ⏱️ Règles temps réelles
		"dtPop" : { "description":"Délai de suppression quand client inactif (en msecs). 0=inactif", "ini":15000, "min":1000, "max":60000, "publish":True },
        "dtIdle" : { "description":"Delai avant passage idle = invisible,invincible mais toujours visible dans viewer (en msecs)", "ini":30000, "min":0, "max":600000, "publish":True },
		"dtPing" : { "?fr":"Delai en msecs entre chaque envoi periodique du state du serveur de jeu", "ini":3000, "min":1000, "max":60000, "publish":False },
		"dtUpdate" : { "?fr":"Delai en msecs entre chaque update du jeu", "ini":100, "min":1000, "max":60000, "publish":False },

		# ⏯️ Règles pour connaitre et changer l'état du jeu 
		"info" : { "?fr":"Message public affiché dans l arene", "ini":"", "publish":True },
		"t" : { "?fr":"Timestamp en msecs depuis le dernier reset", "ini":0, "readonly":True, "publish":True },
		"pause" : { "?fr":"Mettre le jeu en pause", "ini":False, "publish":True },
		"connected" : { "?fr":"Si le jeu est connecté", "readonly":True, "ini":True, "publish":True },
		"open" : { "?fr":"Ouvrir ou fermer les portes de l arene. Une fois fermée, aucun nouveau joueur ne pourra rentrer.", "ini":True, "publish":True },
        "public" : { "?fr":"Si oui ou non l'arene apparait dans la liste des arenes publiques joignables par tous.", "ini":True, "publish":True },
	}
	requests = {
		"reset" : { "?fr":"Supprime tous les players et redemarre le jeu", "reset":True},
		"delPlayer" : { "?fr":"Supprime les players demandés dans une liste de str", "reset":False},
		"addPlayer" : { "?fr":"Ajoute les players demandés dans une liste de str", "reset":False},
		"addAuth" : { "?fr":"Ajoute la clé str recue en liste blanche dans le dico authorised", "reset":False},
		"setAuth" : { "?fr":"Modifie les auths pour chaque player dans le dico spécifié", "reset":False},
		"delAuth" : { "?fr":"Supprime la clé str recue dans le dico authorised", "reset":False},
	}
				
	def __onConnect(client, arena, flags, rc):
		if ( rc == 0 ):
			anx.info("🟢 Arena "+str(arena.__id)+" connected to broker "+arena.__serverAddress+":"+str(arena.__serverPort))
			arena.__isConnectedToBroker = True
			for topic in arena.__topicsToSubscribe:
				anx.info("⏳ Subscribing "+str(arena.__id)+" to topic "+str(topic)+" ...")
				arena.__client.subscribe(topic)
		else:
			anx.error("❌ FAIL to connect  "+str(arena.__id)+" to broker. Returned "+str(rc))
	def __onDisconnect(client, arena, rc):
		anx.warning("🔴 Arena "+str(arena.__id)+" disconnected from broker")
		arena.__isConnectedToBroker = False
	def __onSubscribe(client, arena, mid, granted__qos):
		anx.info("🔔 Subscription of "+str(arena.__id)+" to topic "+str(mid)+" ok")
	def __onUnsubscribe(client, arena, mid):
		anx.info("🔔 Unsubscription of "+str(arena.__id)+" to topic "+str(mid)+" ok")
	def __onMessage(client, arena, msg):
		try:
			payload=str(msg.payload.decode())
			anx.debug("📡 Rx on "+str(msg.topic)+": "+str(payload))
			arena.__messageBufferLock.acquire()
			arena.__messageBuffer.append((msg.topic, payload))
			arena.__messageBufferLock.release()
		except Exception as e:
			anx.error("⚠️ FAIL parsing msg "+str(e)+": "+str(msg.payload))
			anx.error(traceback.format_exc())

	def __init__(self, customRules={}):
		# Init rules from self.__rulesIni dico
		self.__rulesIni = Arena.rules #TODO : expose get/set methods instead of using protected attribute
		for ruleName, rule in customRules.items():
			if ( ruleName not in self.__rulesIni ):
				self.__rulesIni[ruleName] = rule
		self.__rules:dict[str,Any] = {} #TODO : expose get/set methods instead of using protected attribute
		for key, value in self.__rulesIni.items():
			if ( "ini" in value ):
				if ( key in customRules ):
					self.__rules[key] = customRules[key]["ini"]
				else:
					self.__rules[key] = value["ini"]
		for key, value in customRules.items():
			if ( key not in self.__rules ):
				self.__rules[key] = value
		self.__id = self.__rules["arenaName"]
		self.__players:dict[str,IPlayerModel] = {}
		self.__robots:dict[str,IRobotModel] = {}
		self.__isConnectedToBroker = False
		self.__resetRequested = False
		self.__stateHasChanged = False
		self.__pingRequested = False
		self.__verbosity = self.__rules["verbosity"]
		self.__prevReset = datetime.fromtimestamp(0)
		self.__prevPing = datetime.fromtimestamp(0)
		self.__prevRx = datetime.fromtimestamp(0)
		# Set mqtt parameters
		self.__username = self.__rules["username"]
		self.__password = self.__rules["password"]
		self.__serverAddress = self.__rules["brokerAddress"]
		self.__serverPort = self.__rules["brokerPort"]
		self.__topicPlayersRequest = Arena.topicPlayersRequest + "/" + self.__id + "/+"
		self.__topicServerPing = Arena.topicServerPing + "/" + self.__id
		self.__topicServerRequest = Arena.topicServerRequest + "/" + self.__id
		self.__topicServerState = Arena.topicServerState + "/" + self.__id
		self.__topicsToSubscribe = [self.__topicPlayersRequest, self.__topicServerRequest, self.__topicServerPing, Arena.topicRobotsState+"/+"]
		self.__qos = 0
		self.__messageBuffer:list[tuple[str,str]] = []
		self.__messageBufferLock = threading.Lock()
		anx.info("⏳ Arena "+str(self.__id)+" starting on "+str(self.__serverAddress)+" with username "+str(self.__username))
		# Loads
		self.reset()
		# Create mqtt handler
		self.__client = mqtt.Client(client_id = self.__id, userdata=self)
		# Subscribe to callbacks
		self.__client.on_connect = Arena.__onConnect
		self.__client.on_disconnect = Arena.__onDisconnect
		self.__client.on_subscribe = Arena.__onSubscribe
		self.__client.on_unsubscribe = Arena.__onUnsubscribe
		self.__client.on_message = Arena.__onMessage
		# Connect to mqtt server and start communicating
		self.__isLoopStarted = False
		self.start()

	def start(self):
		""" Connect to mqtt server and start communicating """
		if self.__isLoopStarted and self.__isConnectedToBroker:
			return False
		if (self.__username is not None and self.__password is not None):
			self.__client.username_pw_set(self.__username, self.__password)
		try:
			if ( self.__isConnectedToBroker == False ):
				anx.info("⏳ Connecting "+str(self.__id)+" to broker "+self.__serverAddress+":"+str(self.__serverPort)+"...")
				self.__client._connect_timeout = 5.0
				rc=self.__client.connect(self.__serverAddress, self.__serverPort)
			if ( self.__isLoopStarted == False ):
				anx.info("⏳ Starting mqtt thread loop ...")
				self.__client.loop_start()
				anx.info("🟢 Started mqtt loop")
				self.__isLoopStarted = True
			time.sleep(2)
			return rc == 0
		except Exception as e:
			anx.error("⚠️ FAIL connecting "+str(self.__id)+" to broker "+self.__serverAddress+":"+str(self.__serverPort)+": "+str(e))
			return False

	def stop(self):
		"""Arrête la reception et se deconnecte du broker mqtt"""
		anx.info("⏳ Stopping "+str(self.__id)+"...")
		if ( self.__isLoopStarted and self.__isConnectedToBroker ):
			self.__rules['connected'] = False
			state = self.__stateToJson()
			anx.debug("📡 Tx to topic "+str(self.__topicServerState)+": "+str(state))
			self.__client.publish(self.__topicServerState, state, self.__qos)
		if self.__isLoopStarted: 
			anx.info("⏳ Stopping mqtt thread loop ...")
			self.__client.loop_stop(force=True)
			anx.info("🔴 Stopped mqtt thread loop")
			self.__isLoopStarted = False	
		if self.__isConnectedToBroker:
			anx.info("⏳ Disconnecting "+str(self)+" from broker...")
			self.__client.disconnect()
	
	def reset(self):
		"""Reset du jeu"""
		anx.info("⏳ Reseting arena "+self.__id)
		anx.setVerbosity(self.__verbosity)
		self.__players.clear()
		self._onReset(self.__rules)
		self.__stateHasChanged = True
		self.__prevReset = datetime.now()
		
	def update(self):
		"""Actualise les états des players et synchronise avec le server"""
		now = datetime.now()

		#actualise input messages mqtt thread safe
		self.__messageBufferLock.acquire()
		msgBuffer = copy.deepcopy(self.__messageBuffer)
		self.__messageBuffer = []
		self.__messageBufferLock.release()
		for msg in msgBuffer:
			self.__onMessageUpdate(msg[0], msg[1])

		#self.__rules["info"] = "🧑 "+str(len(self.__players))+" player(s)"
		if ( not self.__rules["pause"] ):           
			self._onUpdate(self.__rules, self.__players, self.__robots)

			# players req
			players = list(self.__players.keys())
			for playerClientId in players:
				if ( playerClientId not in self.__players ):
					continue
				player = self.__players[playerClientId]

				# update players
				player.update()
				self._onPlayerUpdate(player, self.__rules, self.__players, self.__robots)
					
				# synchronization with player api, and robots
				if ( self.__isConnectedToBroker ):
					state = player.stateToJson()
					#TODO : check if state changed before publishing
					topic = Arena.topicPlayersState + "/" + self.__id + "/" + player.clientId
					anx.debug("📡🧑 Tx to topic "+str(topic)+": "+str(state))
					self.__client.publish(topic, state, self.__qos)
					request = player.requestToJson(asString=False)
					if ( len(request) > 0 and len(player.robotId) > 0 ):
						request = json.dumps(request)
						topic = Arena.topicRobotsRequest + "/" + player.robotId
						anx.debug("📡🤖 Tx to topic "+str(topic)+": "+str(request))
						self.__client.publish(topic, request, self.__qos)

				# purge players
				if ( player.isConnected() == False ):
					self.__delPlayer(player.clientId)    
					break
				
			# robots req
			for robot in self.__robots.values():
				# purge disconnected robots
				if ( robot.isConnected() == False ):
					self.__delRobot(robot.id)    
					break

		# Envoi l'état du jeu si changement ou periodiquement
		dtPing = (now - self.__prevPing).total_seconds() * 1000
		if ( dtPing > self.__rules["dtPing"] ):
			self.__pingRequested = True
		if ( self.__stateHasChanged or self.__pingRequested ):
			state = self.__stateToJson()
			anx.debug("📡🎲 Tx to topic "+str(self.__topicServerState)+": "+str(state))
			self.__client.publish(self.__topicServerState, state, self.__qos)
			self.__client.publish(Arena.topicRobotsRequest, json.dumps({"ping":True}), self.__qos)
			self.__stateHasChanged = False         
			self.__pingRequested = False      
			self.__prevPing = now
					
		# Redemarre arena si requete reçue
		if ( self.__resetRequested ):
			self.reset()     
			self.__resetRequested = False
					
		time.sleep(self.__rules["dtUpdate"]/1000.0)

	def _onRequestRx(self, key, value):
		"""Can be overriden"""
		try:
			anx.debug("📡🎲 Request "+str(key)+" "+str(value))
			if key == "delPlayer":
				for playerId in value:
					self.__delPlayer(playerId) 
			elif key == "addPlayer":
				for playerId in value:
					self.addPlayer(playerId) 
			elif key == "addAuth":
				self.__rules["authorised"][value] = {"ban":False,"player":value, "robot":"", "team":0, "profile":0}
			elif key == "setAuth":
				for clientId, authValues in value.items():
					if ( clientId not in self.__rules["authorised"] ):
						self.__rules["authorised"][clientId] = {"ban":False,"player":value, "robot":"", "team":0, "profile":0}
					for authKey, authValue in authValues.items():
						if ( authKey not in self.__rules["authorised"][clientId] ):
							continue
						self.__rules["authorised"][clientId][authKey] = authValue
			elif key == "delAuth":
				if ( value in self.__rules["authorised"] ):
					del self.__rules["authorised"][value]
		except Exception as e:
			anx.error("⚠️ FAIL request game with key "+str(key)+": "+str(value))
			anx.error(traceback.format_exc())

	def _onRobotAdded(self, robotId, rules, players, robots):
		"""Can be overriden"""
		return Robot(robotId, self.__rules["dtPop"])

	def _onPlayerAdded(self, clientId, playerId, robotId, rules, players, robots):
		"""Can be overriden"""
		return Player(rules, clientId, playerId, robotId)

	def updateRequest(self, request) -> int:
		self.__prevRx = datetime.now()
		nReq = 0
		for key, value in request.items():
			# If rule change requested
			if ( key in self.__rules ):
				# Read only check
				if ( 'readonly' in self.__rulesIni[key] ):
					if ( self.__rulesIni[key]['readonly'] == True ):
						continue
				# Type check
				if ( type(value) != type(self.__rules[key]) ):
					anx.debug("⚠️ Rx invalid request "+str(key)+"! "+str(value)+" should be "+str(type(self.__rules[key])))
					continue
				# Min max check if value is a number
				if ( "min" in self.__rulesIni[key] and type(value) == int ):
					if ( value < self.__rulesIni[key]["min"] ):
						anx.debug("⚠️ Rx invalid request "+str(key)+"! "+str(value)+" should be between "+str(self.__rulesIni[key]["min"])+" and "+str(self.__rulesIni[key]["max"]))
						continue
				# Min max check if value is a number
				if ( "max" in self.__rulesIni[key] and type(value) == int ):
					if ( value > self.__rulesIni[key]["max"] ):
						anx.debug("⚠️ Rx invalid request "+str(key)+"! "+str(value)+" should be between "+str(self.__rulesIni[key]["min"])+" and "+str(self.__rulesIni[key]["max"]))
						continue
				# Differency check
				if ( value == self.__rules[key] ):
					continue
				# Valid rule change
				anx.info("🎲 Changing arena rules: "+str(key)+"="+str(value))
				nReq += 1
				self.__rules[key] = value
				self.__stateHasChanged = True
				# Request reset
				if ( "reset" in self.__rulesIni[key] ):
					if ( self.__rulesIni[key]["reset"] == True ):
						self.__resetRequested = True
			# If others allowed requests
			elif ( key in Arena.requests ):
				nReq += 1
				self._onRequestRx(key, value)
				# Request reset
				if ( "reset" in Arena.requests[key] ):
					if ( Arena.requests[key]["reset"] == True ):
						self.__resetRequested = True
			# Request on playerState
			elif ( key == "playerState" ):
				nReq += 1
				try:
					for clientId, playerReq in value.items():
						anx.debug("🎲 Changing player state: "+str(clientId)+"="+str(playerReq))
						if ( clientId not in self.__players ):
							if ( self.addPlayer(clientId) == None ):
								continue
						playerToRule = self.__players[clientId]
						playerToRule.updateState(playerReq) 
				except:
					...
			# Request on playerRequest
			elif ( key == "playerRequest" ):
				nReq += 1
				try:
					for clientId, playerReq in value.items():
						anx.debug("🎲 Changing player request: "+str(clientId)+"="+str(playerReq))
						if ( clientId not in self.__players ):
							continue
						playerToRule = self.__players[clientId]
						playerToRule.updateRequest(playerReq) 
				except:
					...
		return nReq

	def __onMessageUpdate(self, topic, payload):
		"""Parse message reçu pour actualiser le jeu"""
		# Message reçu de player
		if ( topic.find(Arena.topicPlayersRequest) == 0):        
			topicsplit = topic.split('/')
			topicPlayersRequestsplit = Arena.topicPlayersRequest.split('/')
			lensplit = len(topicPlayersRequestsplit)+2
			if (len(topicsplit) != lensplit ):
				anx.debug("⚠️ Rx incorrect topic "+str(topic))
				return
			playerId = topicsplit[lensplit-1]
			if ( playerId not in self.__players ):
				self.addPlayer(playerId)
			if ( playerId in self.__players ):
				request = json.loads(payload)
				self.__players[playerId].updateRequest(request)
		# Message reçu de robot
		elif ( topic.find(Arena.topicRobotsState) == 0):        
			topicsplit = topic.split('/')
			topicRobotsStateSplit = Arena.topicRobotsState.split('/')
			lensplit = len(topicRobotsStateSplit)+1
			if (len(topicsplit) != lensplit ):
				anx.debug("⚠️ Rx incorrect topic "+str(topic))
				return
			robotId = topicsplit[lensplit-1]
			if ( robotId not in self.__robots ):
				self.__addRobot(robotId)
			if ( robotId in self.__robots ):
				state = json.loads(payload)
				self.__robots[robotId].updateState(state)
		# Message reçu de admin
		elif ( topic == self.__topicServerRequest ):
			request = json.loads(payload)
			self.updateRequest(request)            
		# Ping recu
		elif ( topic == self.__topicServerPing ):
			self.__pingRequested = True

	def __addRobot(self, robotId):
		if ( len(self.__robots) >= self.__rules["maxRobots"] ):
			anx.debug("⚠️ FAIL to add robot "+str(robotId)+". Limit of "+str(self.__rules["maxRobots"])+" robots reached.")
			return
		# Look if robot authorised to join in this arena
		robotAuth = True
		if ( self.__rules["onlyAuthorised"] ):
			robotAuth = False
			for clientId in self.__rules["authorised"]:
				if "robot" in self.__rules["authorised"][clientId] and self.__rules["authorised"][clientId]["robot"] == robotId:
					robotAuth = True
					break
		if ( robotAuth == False ):
			anx.debug("⚠️ FAIL to add robot "+str(robotId)+". Not authorised.")
			return
		anx.info("🤖🟢 Adding robot "+str(robotId))
		# TODO here: tx tx_rates to
		topic = Arena.topicRobotsRequest + "/" + robotId
		req = json.dumps({"conf": {"tx_rates": 100}})
		anx.debug("📡 Tx to topic "+str()+": "+str(req))
		self.__client.publish(topic, req, self.__qos)
		self.__stateHasChanged = True
		self.__robots[robotId] = self._onRobotAdded(robotId, self.__rules, self.__players, self.__robots)

	def __delRobot(self, robotId):
		if ( robotId in self.__robots ):
			anx.info("🤖🔴 Removing robot "+str(robotId))
			robot = self.__robots.pop(robotId)
			self._onRobotRemoved(robot)
			self.__stateHasChanged = True

	def addPlayer(self, clientId, pnj=False):
		if ( self.__rules["open"] == False ):
			anx.debug("⚠️ FAIL to add player for client id "+str(clientId)+". Arena closed.")
			return
		if ( len(self.__players) >= self.__rules["maxPlayers"] ):
			anx.debug("⚠️ FAIL to add player for client id "+str(clientId)+". Limit of "+str(self.__rules["maxPlayers"])+" player reached.")
			return None
		elif ( self.__rules["onlyAuthorised"] == True and (clientId not in self.__rules["authorised"] or self.__rules["authorised"][clientId]["ban"]==True) ):
			anx.debug("⚠️ FAIL to add player for client id "+str(clientId)+". NOT AUTHORISED.")
			return None
		if ( len(clientId) >= self.__rules["nameLen"] ):
			anx.debug("⚠️ FAIL to add player for client id "+str(clientId)+". Name too long.")
			return None
		playerId = clientId
		robotId = ""
		if ( clientId in self.__rules["authorised"] ):
			if ( pnj == False and 'pnj' in self.__rules["authorised"][clientId] and 
       			 self.__rules["authorised"][clientId]["pnj"] == True ):
				anx.debug("⚠️ FAIL to add player for client id "+str(clientId)+". Reserved for pnj.")
				return None
			if ( 'player' in self.__rules["authorised"][clientId] ):
				playerRequested = self.__rules["authorised"][clientId]['player']
				if ( type(playerRequested) is str ):
					playerId = playerRequested
			if ( 'robot' in self.__rules["authorised"][clientId] ):
				playerRequested = self.__rules["authorised"][clientId]['robot']
				if ( type(playerRequested) is str ):
					robotId = playerRequested
		anx.info("🧑🟢 Adding player "+str(playerId)+" for client "+str(clientId) + " associated with robot "+str(robotId))
		self.__players[clientId] = self._onPlayerAdded(clientId, playerId, robotId, self.__rules, self.__players, self.__robots)
		self.__stateHasChanged = True
		return self.__players[clientId]

	def __delPlayer(self, playerId):
		if ( playerId in self.__players ):
			anx.info("🧑🔴 Removing player "+str(playerId)+" for client "+str(self.__players[playerId].clientId) + " associated with robot "+str(self.__players[playerId].robotId))
			player = self.__players.pop(playerId)
			self._onPlayerRemoved(player)
			self.__stateHasChanged = True

	def __stateToJson(self):
		# Add actual players to state
		now = datetime.now()
		state = {}
		state['players'] = []
		for playerName in self.__players.keys():
			state['players'].append(playerName)
		state['robots'] = []
		for robotName, robot in self.__robots.items():
			state['robots'].append(robot.stateToJson(asString=False))
		# Add actual rules to state
		for key,value in self.__rules.items():
			if ( key in self.__rulesIni and "publish" in self.__rulesIni[key] and self.__rulesIni[key]["publish"] == True ):
				state[key] = value
		state['nPlayers'] = len(state['players'])
		state['nRobots'] = len(state['robots'])
		state['t'] = int((now - self.__prevReset).total_seconds() * 1000)
		return json.dumps(state)   

	def __run__(filepath:str="settings.json"):
		"""
		Launch arena from json file
		settings.json file describing the arena credentials, rules ... with at least the following keys: 
		|_ 'logDir' :          The dirname of the dir that will include log files. Do not include abs path, only dir name.
		|_ 'arena' :           The name of the arena
		|_ 'factoryFolder' :   The folder in which an .py script describes the Arena class to instanciate
		|_ 'factoryFile' :     The .py script describing the Arena class to instanciate
		|_ 'factoryClass' :    The Arena class name to instanciate
		|_ 'username' :        To log in the mqtt broker
		|_ 'password' :        To log in the mqtt broker
		|_ 'brokerAddress' :   As url or ip address without including the protocol
		|_ 'brokerPort' : 	   To connect to mqtt broker on the specified brokerAddress
		|_ 'viewerPort' : 	   To see the arena viewer using an http webviewer
		|_ 'rules' : 		   A dict of game rules keys values
		|_ 'restartOnExcept' : To enable auto retart when an exception is raised
		|_ 'verbosity' :       An integer to set the verbosity of the arena logs, from 0 (no log), to 4 (all)
		"""
		restartOnExcept = True
		while restartOnExcept:
			arenaInfos = {}
			anx.setVerbosity(anx.Verbosity.INFO)
			anx.info("⏳ Loading arena infos from "+str(filepath))
			try:
				with codecs.open(filepath, "r", "utf-8-sig") as file:
					content = file.read()
					arenaInfos = json.loads(content)
					anx.info("⏳ Loading arena infos: "+str(arenaInfos))
					file.close()
				arenaInfos = arenaInfos["arena"]
			except Exception as e:
				anx.error("❌ FAIL loading "+filepath+" : "+str(e))
			restartOnExcept = False
			if ( "restartOnExcept" in arenaInfos ):
				restartOnExcept = arenaInfos["restartOnExcept"]["ini"]
			anx.setLogger(anx.FileLogger(
				anx.Verbosity.WARNING, 
				os.path.join(arenaInfos["logDir"]["ini"],arenaInfos["arenaName"]["ini"]+str(datetime.now()).replace(" ","_").replace(":","-")+".log"))
			)
			arenaConstructor = getattr(
				getattr(
					__import__(arenaInfos["factoryDir"]["ini"], fromlist=[arenaInfos["factoryFile"]["ini"]]), 
					arenaInfos["factoryFile"]["ini"]
				),
				arenaInfos["factoryClass"]["ini"]
			)
			arena = arenaConstructor(customRules=arenaInfos)
			if ( restartOnExcept ):
				try:
					while True:
						arena.update()
				except Exception as e:
					anx.error("🔴 EXCEPTION raised while updating arenas: "+str(e))
					anx.error(traceback.format_exc())
					anx.error("Rebooting arena...")
					arena.stop()
					time.sleep(3)
			else:			
				while True:
					arena.update()

if __name__ == '__main__':
    anx.warning("⚠️ Nothing to run from lib "+str(__file__))