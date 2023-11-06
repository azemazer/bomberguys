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

import json
from datetime import datetime
from typing import Any 

class IRobotModel:
	def __init__(self,id):
		self.id:str = id
		self.battery:int = 0
		self.photoFront:int = 0
		self.photoBack:int = 0
		self.t:int = 0
	def isConnected(self):
		...
	def updateState(self, state:dict[str,Any]):
		...
	def stateToJson(self, asString=True):
		...	

class Robot(IRobotModel):
	def __init__(self, id:str, dtDisconnect:int=5000):
		if ( dtDisconnect == 0 ):
			dtDisconnect = 5000
		super().__init__(id)
		now = datetime.now()
		self.__dtDisconnect:int = dtDisconnect
		self.__prevRx = now
	def isConnected(self):
		return (datetime.now()-self.__prevRx).total_seconds() * 1000 < self.__dtDisconnect
	def updateState(self, state:dict[str,Any]):
		self.__prevRx = datetime.now()
		if ( 'battery' in state and type(state['battery'])==int):
			self.battery = state["battery"]
		if ( 'photoBack' in state and 'lum' in state['photoBack'] and type(state['photoBack']['lum'])==int):
			self.photoBack = state['photoBack']['lum']
		if ( 'photoFront' in state and 'lum' in state['photoFront'] and type(state['photoFront']['lum'])==int):
			self.photoFront = state['photoFront']['lum']
		if ( 't' in state and type(state['t'])==int):
			self.t = state['t']
	def stateToJson(self, asString=True):
		state = {}
		state['id'] = self.id
		state['battery'] = self.battery
		state['connected'] = self.isConnected()
		if ( asString ):
			return json.dumps(state)
		else:
			return state