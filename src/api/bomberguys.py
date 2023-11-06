from typing import Any
import j2l.pytactx.agent as pytactx
from enum import Enum

class Tile(Enum):
    
    empty = 0
    bomb = 1
    ironBlock = 2
    stoneBlock = 3
    alliedPlayer = 4
    ennemyPlayer = 5
    explosion = 6

class IBomberGuy:

    def __init__(self):
        self.clientId : str = ""
        self.playerId : str = ""
        self.robotId : str = ""
        self.team : int = 0
        self.profile : int = 0
        self.x : int = 0
        self.y : int = 0
        self.map : tuple[tuple[Tile]] = []
        self.gridColumns : int = 10
        self.gridRows : int = 10
        self.bombCooldown : int = 0
    
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

    def dropBomb() -> None:
        """
        Drops a bomb with a 5s countdown.
        The request will be send the next update() call
        """

class PytactXBomberGuy(IBomberGuy):
    def __init__(self, playerID, arena, server, port, username, verbosity, password):
        super().__init__()
        self.__agent = pytactx.Agent(
            playerId    =   playerID,
            server      =   server,
            arena       =   arena,
            username    =   username,
            password    =   password,
            port        =   port,
            verbosity   =   verbosity
        )