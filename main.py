from typing import Any
import j2l.pytactx.agent as pytactx
import random
import copy

# agent.robot.playMelody([('C5', 200) , ('G4', 100) , ('G4', 100) , ('G#4', 200) , ('G4', 400) ,('B4', 200) , ('C5', 200) ])
def findCloserAgentPos(dict: dict, currentAgentX: int, currentAgentY: int) -> tuple:
    closerNeighbourName = ''
    closerNeighbourTotalDiff = 100
    for neighbourName, neighbourStats in dict.items() :
        diffX = abs(neighbourStats['x']-currentAgentX)
        diffY = abs(neighbourStats['y']-currentAgentY)
        totalDiff = diffX + diffY
        if (totalDiff < closerNeighbourTotalDiff) :
            closerNeighbourName = neighbourName
    return (dict[closerNeighbourName]['x'], dict[closerNeighbourName]['y'])
        


class IState:
	def doAction():
		...

class ScanState(IState):
	def __init__(self, agent) -> None:
		self.__agent = agent
	def doAction(self):
		if (self.__agent.range != {}):
			self.__agent.setState(AttackState(self.__agent))
		else:
			self.__agent.setColor(0, 255, 0)
			self.__agent.fire(False)
			self.__agent.lookAt(random.randint(0,3))
			self.__agent.move(random.randint(-1,1), random.randint(-1,1))

class AttackState(IState):
	def __init__(self, agent) -> None:
		self.__agent = agent
	
	def doAction(self):
		if (self.__agent.range == {}):
			self.__agent.setState(ScanState(self.__agent))
		else :
			self.__agent.setColor(255, 0, 0)
			self.__agent.fire(True)
			coordonneesToAttack = findCloserAgentPos(copy.deepcopy(self.__agent.range), self.__agent.x, self.__agent.y)
			self.__agent.moveTowards(coordonneesToAttack[0], coordonneesToAttack[1])


class StateMachine:
	def __init__(self) -> None:
		self.__actualState = None
	def setState(self, newState: IState):
		self.__actualState = newState
	def doCurrentAction(self):
		self.__actualState.doAction()
	
 
class SpecialAgent(pytactx.Agent):
	def __init__(self, playerId: str = None, arena: str = None, username: str = None, password: str = None, server: str = None, port: int = 1883, imgOutputPath: str = "img.jpeg", autoconnect: bool = True, useProxy: bool = True, verbosity: int = 3, robotId: str = "_", welcomePrint: bool = True, sourcesdir: str = None):
		super().__init__(playerId, arena, username, password, server, port, imgOutputPath, autoconnect, useProxy, verbosity, robotId, welcomePrint, sourcesdir)
		self.__fsm = StateMachine()
		self.__fsm.setState(ScanState(self))
	def _onUpdated(self, eventSrc: Any, eventName: str, eventValue: Any):
		self.__fsm.doCurrentAction()
		# Ne pas oublier d'appeler la méthode de la classe mère
		# pour ne pas écraser les fonctionnalités existantes
		return super()._onUpdated(eventSrc, eventName, eventValue)
	def setState(self, newState: IState):
		self.__fsm.setState(newState)
	
agent = SpecialAgent(playerId='Alexandre',
						arena='creativecda2324',
						username="demo",
						password=input("🔑 password: "),
						server="mqtt.jusdeliens.com",
						verbosity=3)

agent.update()
print(agent.game)

while True:
	agent.update()
	agent.lookAt((agent.dir+1)%4)
