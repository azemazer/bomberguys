from typing import Any
import j2l.pytactx.agent as pytactx
from enum import Enum
import time

class Tile(Enum):
    
    empty = 0
    bomb = 1
    ironBlock = 2
    stoneBlock = 3
    alliedPlayer = 4
    ennemyPlayer = 5
    explosion = 6

class IBomberGuy:

    # GETTERS 

    def getTile(self, x: int, y:int) -> list[int]:
        """
        Gets the tile located at a given location.
        Returns a list of items positionned at said location.
        empty = 0
        bomb = 1
        ironBlock = 2
        stoneBlock = 3
        alliedPlayer = 4
        ennemyPlayer = 5
        explosion = 6
        """
        ...

    def getTeam(self) -> int:
        """
        Gets the team of the agent.
        """
        ...
    def getX(self) -> int:
        """
        Gets the X location of the agent.
        """
        ...
    def getY(self) -> int:
        """
        Gets the X location of the agent.
        """
        ...    
    def getColor(self) -> tuple:
        """
        Gets the color of the agent.
        """
        ...    
    def getBombCooldown(self) -> int:
        """
        Gets the bomb cooldown of the agent. It lasts 5 seconds
        and starts as soon as the agent drops a bomb.
        If the bomb is on cooldown, the agent cannot
        drop a bomb.
        """
        ...

        # METHODS
    
    def update(self) -> None :
        """
        Fetch the last values of robot sensors from server
        And send buffered requests in one shot to limit bandwidth.
        To be call in the main loop at least every 10 msecs.
        """

    def move(self,dx:int,dy:int) -> None:
        """
        Request a relative moves on the grid around the previous agent position 
        according to the specified dx, dy values.
        The request will be send the next update() call
        """

    def setColor(self, r:int, g:int, b:int) -> None:
        """
        Request a color change for the robot led
        The request will be send the next update() call
        """

    def dropBomb(self) -> None:
        """
        Drops a bomb with a 5s countdown.
        The request will be send the next update() call
        """

class PytactXBomberGuy(IBomberGuy):
    def __init__(self, playerID, arena, server, username, verbosity, password, port):
        self.__agent = pytactx.Agent(
            playerId    =   playerID,
            server      =   server,
            arena       =   arena,
            username    =   username,
            password    =   password,
            port        =   port,
            verbosity   =   verbosity
        )
        self.__bombCooldown = 0
        while len(self.__agent.map) == 0:
            self.__agent.lookAt((self.__agent.dir)%4)
            self.__agent.update()
    

    # GETTERS 

    def getTile(self, x: int, y:int) -> list[int]:
        if "map" not in self.__agent.game:
            return []
        if y >= len(self.__agent.game["map"]):
            return []
        if x >= len(self.__agent.game["map"][y]):
            return []
        return self.__agent.game["map"][y][x]
    
    def getMap(self) -> list[list[int]]:
        if "map" not in self.__agent.game:
            return []
        return self.__agent.game["map"]

    def getTeam(self) -> int:
        return self.__agent.team

    def getX(self) -> int:
        return self.__agent.x

    def getY(self) -> int:
        return self.__agent.y
    
    def getColor(self) -> tuple:
        return self.__agent.color
    
    def getBombCooldown(self) -> int:
        return self.__bombCooldown 
    
    # METHODS

    def update(self) -> None:
        self.__agent.update()
        time.sleep(0.3)

    def move(self, dx: int, dy: int) -> None:
        return self.__agent.move(dx, dy)

    def setColor(self, r:int, v:int, b:int) -> None:
        return self.__agent.setColor(r, v, b)
    
    def dropBomb(self) -> None:
        return self.__agent.fire(True)
    
    def printInfos(self) -> None:
        return print(self.__agent.game)
