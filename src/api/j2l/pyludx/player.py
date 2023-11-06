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

import base64
import json
from datetime import datetime
import os
import threading 
from pathlib import Path
from typing import Any
import base64
import codecs
import threading
import pyanalytx.logger as anx

class IPlayerModel:
	"""
	Model class that stores informations about player agent in the arena
	This base class can be inherited and its methods overriden
	If so, don't forget to instanciate the derivated class when
	_onPlayerAdded its called from Arena inherited class
	"""
	def __init__(self, clientId:str, playerId:str, robotId:str):
		self.clientId	: str 					= clientId
		self.playerId	: str 					= playerId
		self.robotId	: str 					= robotId	# Stats des code recus
		self.nExe 		: int 					= 1			# Stats du nombre de fois où le code de l'agent a été démarré
		self.src 		: list[dict[str,Any]] 	= []
	def _onStateToJson(self) -> dict[Any,Any]:
		"""
		Returns the extended state of the player as a dict of key value pairs
		To be overriden
		"""
		return {}
	def _onUpdate(self) -> None:
		"""
		Call when updating auto behaviour of the player 
		To be overriden
		"""
		...
	def _onUpdateRequest(self, request:dict[Any,Any]) -> int:
		"""
		Returns the number of requests performed
		To be overriden
		"""
		...
	def _onUpdateState(self, state:dict[Any,Any]) -> int:
		"""
		Returns the number of state modified
		To be overriden
		"""
		...
	def isConnected(self) -> bool:
		"""
		False if nothing rx from player after dtPop ms
		"""
		...
	def isIdle(self) -> bool:
		"""
		True if nothing rx from player after dtIdle ms
		"""
		...
	def update(self) -> None:
		"""
		Update auto behaviour of the player like ia or inertial effects
		"""
		...
	def updateRequest(self, request:dict[str,Any]) -> int:
		"""
		Change player request to be taken into account the next game update
		according to the key values specified
		To be used to handle req from client API
		Returns the number of state modified
		"""
		...
	def stateToJson(self,asString=True) -> dict[str,Any] or str:
		...
	def updateState(self, state:dict[Any,Any]) -> int:
		"""
		Change player state according to the key values specified
		To be used to handle ruleAgent req from client API
		Returns the number of state modified
		"""
		...
	def requestToJson(self,asString=True, pop=True) -> dict[str,Any]:
		...


def saveSrc(srcDirPath, srcFileName, makesubdirs, srcContent, playerId):
    try:
        if ( makesubdirs ):
            path = Path(srcDirPath)
            path.mkdir(parents=True, exist_ok=True)
        with codecs.open(os.path.join(srcDirPath, srcFileName), "w", "utf-8-sig") as f:
            f.write(srcContent)
    except Exception as e:
        anx.warning("⚠️ FAIL saving script of player "+playerId+": "+str(e))


class Player(IPlayerModel):
	def __init__(self, rules:dict[str,Any], clientId:str, playerId:str, robotId:str):
		super().__init__(clientId, playerId, robotId)
		now = datetime.now()
		self.__reqRobotBuf:dict[str,Any] = {}
		self.__prevRx = now
		self.__rules = rules
		self.__prevState = ""
	def isIdle(self) -> bool:
		return (datetime.now()-self.__prevRx).total_seconds() * 1000 >= self.__rules["dtIdle"]
	def isConnected(self) -> bool:
		return (datetime.now()-self.__prevRx).total_seconds() * 1000 < self.__rules["dtPop"] or self.__rules["dtPop"] == 0
	def update(self) -> None:
		self._onUpdate()
	def updateRequest(self, request:dict[str,Any]) -> int:
		nReq = 0
		# Deals with robot request here
		if ( 'led' in request ):
			# TODO here : when rx tuple rgb set static anim
			# BUT when dict send request has it is to robot
			try:
				if ( isinstance(request["led"],list) and len(request["led"]) == 3 ):
					self.__reqRobotBuf['led'] = {
						"animation": "static", 
						"rgb":request["led"]
					}
				elif ( isinstance(request["led"],dict) and "animation" in request["led"] ):
					self.__reqRobotBuf['led'] = request["led"]
				nReq += 1
			except:
				...
		if ( 'buzzer' in request and len(request["buzzer"]) >= 1 ):
			tones = []
			for tone in request["buzzer"]:
				if ( len(tone) == 2 ):
					tones.append(tone)
			self.__reqRobotBuf['buzzer'] = tones
			nReq += 1
		if ( 'motor' in request ):
			self.__reqRobotBuf['motor'] = request["motor"]
			nReq += 1
		# Deals with src run requests
		if ( 'nExe' in request ):
			# Fetch sources from player
			nChars = 0
			try:
				srcs = request["nExe"]
				for srcPathIn, srcInfo in srcs.items():
					srcSubdirs, srcFilename, srcExt, srcContent = srcInfo[0], srcInfo[1],srcInfo[2],srcInfo[5]
					if ( len(self.__rules["srcExts"]) > 0 and srcExt not in self.__rules["srcExts"] ):
						continue
					srcCreated = datetime.fromtimestamp(srcInfo[3]).strftime('%Y-%m-%d_%H-%M-%S')
					srcModified = datetime.fromtimestamp(srcInfo[4]).strftime('%Y-%m-%d_%H-%M-%S')
					makesubdirs = self.__rules["logDir"]
					srcDirPath = self.__rules["saveSrcDir"]
					srcFilenameOut = self.__rules["arenaName"]+'__'+self.playerId+'__'+str(self.nExe)+'__'+srcFilename+srcExt
					if ( makesubdirs ):
						srcDirPath = os.path.join(self.__rules["logDir"], self.__rules["arenaName"], self.playerId, str(self.nExe),*srcSubdirs)
						srcFilenameOut = srcFilename+srcExt
					srcContent = base64.b64decode(srcContent).decode('utf-8')
					nChars+=len(srcContent)
					# Save srcs into dirs
					if ( self.__rules["saveSrc"] and self.clientId in self.__rules["authorised"] and
						(self.__rules["saveNb"] == 0 or self.nExe < self.__rules["saveNb"]) ):
						threading.Thread(target=saveSrc, args=(srcDirPath, srcFilenameOut, makesubdirs, srcContent, self.playerId)).start()
			except Exception as e:
				anx.warning("⚠️ FAIL saving script of player "+self.playerId+": "+str(e))
			# Add stats
			pChars = 0
			dtSrc = 0
			now = datetime.now()
			if ( len(self.src) > 0 ):
				prevSrc = self.src[len(self.src)-1]
				pChars = int(100*(nChars-prevSrc["nChar"])/(nChars+1))
				dtSrc = int((now-datetime.fromtimestamp(prevSrc["t"])).total_seconds()*1000)
			self.src.append({
				"nChar": nChars,
				"pChar": pChars,
				"t": now.timestamp(),
				"dt": dtSrc
			})
			while ( len(self.src) > self.__rules["saveNb"] and self.__rules["saveNb"] > 0 ):
				del self.src[0]
			self.nExe += 1 
		# open to extension
		nReq += self._onUpdateRequest(request)
		if ( nReq > 0 ):
			self.__prevRx = datetime.now()

	def stateToJson(self,asString=True) -> dict[str,Any] or str:
		# open to extension
		state = self._onStateToJson()
		# set base state
		state['clientId'] = self.clientId
		state['playerId'] = self.playerId
		state['robotId'] = self.robotId
		state['connected'] = self.isConnected()
		state['idle'] = self.isIdle()
		state['nExe'] = self.nExe
		state['src'] = self.src
		if ( asString ):
			return json.dumps(state)
		else:
			return state
	def updateState(self, state):
		nState = 0
		nState += self._onUpdateState(state)
		if ( nState > 0 ):
			self.__prevState = state
		return nState
	def requestToJson(self,asString=True, pop=True) -> dict[str,Any]:
		request = self.__reqRobotBuf
		if ( pop ):
			self.__reqRobotBuf = {}
		if ( asString ):
			return json.dumps(request)
		else:
			return request
	