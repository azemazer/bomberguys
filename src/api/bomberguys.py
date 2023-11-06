from typing import Any
import j2l.pytactx.agent as pytactx

class IBomberGuy:

    def __init__(self):
        self.clientId : str = ""
        self.playerId : str = ""
        self.robotId : str = ""
        self.team : int = 0
        self.profile : int = 0
        self.x : int = 0
        self.y : int = 0
        self.color : tuple[int,int,int] = (0,255,0)
        self.score : int = 0
        self.rank : int = 0
        self.game : dict[str,Any] = {}
        self.players : list[str] = []
        self.robots : list[str] = []
        self.map : tuple[tuple[int]] = []
        self.gridColumns : int = 10
        self.gridRows : int = 10
        self.bombCooldown : int = 0

    def connect(self) -> bool :
        """
        Connect the client to the broker.
        Should be called once just after the __init__
        """
    
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

    