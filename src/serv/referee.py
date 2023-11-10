import j2l.pytactx.agent as pytactx
import os
import time
import copy

from dotenv import load_dotenv
load_dotenv()
AGENT_PASSWORD = os.getenv('__AGENT_PASSWORD__')
SERVER = os.getenv('__SERVER__')
PORT = os.getenv('__PORT__')
USERNAME = os.getenv('__USERNAME__')
ARENA = os.getenv('__ARENA__')
ARBITRE_USERNAME = os.getenv('__ARBITRE_USERNAME__')

class Referee:
    def __init__(self, 
                playerId: str, 
                arena: str, 
                username: str, 
                password: str, 
                server: str, 
                port: int, 
                stoneBlockFrequency: float = 0.4,
                bombCountdown: int = 10
                ):
        self.__agent = pytactx.Agent(
            playerId=playerId,
            arena=arena,
            username=username,
            password=password,
            server=server,
            port=port,
        )
        self.__oldRange = {}
        self.__newRange = {}
        self.__stoneBlockFrequency = stoneBlockFrequency
        self.__bombCountdown = bombCountdown
        self.__fsmState = "Initiating"
        self.__team0IsAlive = False
        self.__team1IsAlive = False

    def sleepAndUpdate(self, sleepTime: float = 0.3):

        time.sleep(sleepTime)
        self.__agent.update()

    def bombExplode(self, x: int, y: int) -> None:

        # If a stone block is on an explosion,
        # It disappears

        explosionZone = [(x,y), (x-1,y), (x+1,y), (x,y-1), (x,y+1)]
        map = copy.deepcopy(self.__agent.map)
        for tile in explosionZone:
            mapX, mapY = tile[0], tile[1]
            if  mapY in range(len(map)) and mapX in range(len(map[mapY])) and map[mapY][mapX] == 1:
                map[mapY][mapX] = 0
        self.__agent.ruleArena("map", map)

        # If an agent is on an explosion,
        # He dies

        for player, playerStats in self.__agent.range.items():
            for tile in explosionZone:
                if (playerStats["x"] == tile[0]) and (playerStats["y"] == tile[1]):
                    self.__agent.rulePlayer(player, "life", 0)
    
    def spawnStoneBlocks(self, spawnFrequency: int):
        self.__agent.ruleArena("mapImgs", [
                        "",
                        "stoneblock.jpg",
        ])

        self.__agent.ruleArena("mapRand", True)

        self.__agent.ruleArena("mapRandFreq", spawnFrequency)
        
    def setBombRules(self, bombCountdown):
        bombRuleset = {
        "profiles" : "bomb",
        "pIcons" : "💣",
        "pImgs" : "bomb.svg", 
        "range" : 0,
        "dtDir" : 100,
        "dtMove" : 100,
        "dtFire" : 100,
        "fxFire" : 0,
        "hitFire" : 0,
        "hitCollision" : 0,
        "dxMax" : 0,
        "dyMax" : 0,
        "lifeIni" : bombCountdown, # Is used for the bomb countdown.
        "ammoIni" : 0,
        "invisible" : False,
        "invincible" : False,
        "infiniteAmmo" : False,
        "collision" : True, # You can step over bombs.
        "nRespawn" : 1
                   }
    
        for ruleKey, ruleValue in bombRuleset.items():
            ruleActualValues = self.__agent.game[ruleKey]
            ruleActualValues[1] = ruleValue
            self.__agent.ruleArena(ruleKey, ruleActualValues)

    def setAgentRules(self):

        dtFires = self.__agent.game["dtFire"]
        infiniteAmmos = self.__agent.game["infiniteAmmo"]
        nRespawns = self.__agent.game["nRespawn"]
        # weaponss = self.__agent.game["weapons"]
        dtFires[0] = 5000 # Bomb cooldown for default players
        infiniteAmmos[0] = False # Players don't have limited ammo so we can listen to their number of shoots
        nRespawns[0] = 1 # Players respawn only once
        # weaponss[0] = 0 # Players don't really "shoot"
        self.__agent.ruleArena("dtFire", dtFires)
        self.__agent.ruleArena("infiniteAmmo", infiniteAmmos)
        self.__agent.ruleArena("nRespawn", nRespawns)
        # self.__agent.ruleArena("weapons", weaponss)

    def setArenaRules(self):

        self.__agent.ruleArena("mapImgs", [
                        "",
                        "stoneblock.jpg",
                        "ironblock.jpg",
                        "hit.jpg"
        ])

        self.__agent.ruleArena("mapFriction", [
                            0.0,
                            1.0,
                            1.0,
                            0.0
        ])

        self.__agent.ruleArena("mapRand", False)

        self.__agent.ruleArena("mapRandFreq", 0.0)

        self.__agent.ruleArena("teamColor", [[0, 255, 255], [255, 0, 255]])

        self.__agent.ruleArena("teamName", ["Cyan", "Purple"])

    def spawnIronBlocks(self):

        ironBlockPosX = (1, 3, 5, 7, 9, 11, 13)
        ironBlockPosY = (1, 3, 5, 7, 9)
        ironBlockPos = []
        for xPos in ironBlockPosX:
            for yPos in ironBlockPosY:
                ironBlockPos.append((xPos, yPos))

        map = copy.deepcopy(self.__agent.game["map"])
        for pos in ironBlockPos:
            mapX, mapY = pos[0], pos [1] 
            map[mapY][mapX] = 2

        self.__agent.ruleArena("map", map)

    def spawnPlayers(self):
        agents =  {
            "joueur1": {
                "team": 0,
                "x": 2,
                "y": 2
            },
            "joueur2": {
                "team": 0,
                "x": 2,
                "y": 4
            },
            # "joueur3": {
            #     "team": 0,
            #     "x": 3,
            #     "y": 7
            # },
            "joueur4": {
                "team": 1,
                "x": 12,
                "y": 2
            },
            "joueur5": {
                "team": 1,
                "x": 12,
                "y": 4
            },
            # "joueur6": {
            #     "team": 1,
            #     "x": 13,
            #     "y": 7
            # }
        }

        for agentId, attributes in agents.items():
            for attributeKey, attributeValue in attributes.items():
                self.__agent.rulePlayer(agentId, attributeKey, attributeValue)

    def initArena(self):
        
        #  Spawns random stoneblocks
        self.spawnStoneBlocks(self.__stoneBlockFrequency)

        self.__agent.ruleArena("reset", True)
        self.__agent.update()
        self.sleepAndUpdate(5.0)
        
        # Set bomb rules
        self.setBombRules(self.__bombCountdown)
        self.sleepAndUpdate()

        # Set agents rules
        self.setAgentRules()
        
        # Set Arena rules
        self.setArenaRules()
        self.sleepAndUpdate()
        
        # Spawn iron blocks
        self.spawnIronBlocks()
        self.sleepAndUpdate()
        
        # Spawn players
        self.spawnPlayers()

        # Set inGame state
        self.__fsmState = "inGame"

    def checkIfVictory(self):
        if self.__team0IsAlive and self.__team1IsAlive:
            infoScores = "Game: ongoing"
            self.__agent.ruleArena("info", infoScores)
        else:
            if not self.__team0IsAlive and not self.__team1IsAlive:
                infoScores = "GAME RESULT: DRAW!"
            elif self.__team0IsAlive and not self.__team1IsAlive:
                infoScores = "GAME RESULT: TEAM 1 WON!"
            elif not self.__team0IsAlive and self.__team1IsAlive:
                infoScores = "GAME RESULT: TEAM 2 WON!"
            self.__agent.ruleArena("info", infoScores)
            self.initArena()

    def startRoutine(self):
        self.__agent.lookAt((self.__agent.dir+1)%4)
        self.__newRange = copy.deepcopy(self.__agent.range)

    def endRoutine(self):
        self.checkIfVictory()
        self.__oldRange = self.__newRange
        self.sleepAndUpdate()


    def teamPointsCounter(self, playerStats):
        if playerStats["team"] == 0:
            self.__team0IsAlive = True
        if playerStats["team"] == 1:
            self.__team1IsAlive = True

    def bombDrops(self, player, playerStats):
         if player in self.__oldRange and self.__oldRange[player]["nFire"] < playerStats["nFire"]:
            bombName = player + "b"
            if (bombName in self.__newRange and self.__newRange[bombName]["life"] <= 0) or (bombName not in self.__newRange):
                self.__agent.rulePlayer(bombName, "profile", 1)
                self.__agent.rulePlayer(bombName, "x", playerStats["x"])
                self.__agent.rulePlayer(bombName, "y", playerStats["y"])
                self.__agent.rulePlayer(bombName, "life", 10)

    def bombExplodes(self, playerStats):
        if playerStats["profile"] == 1:
            bombLife = playerStats["life"]
            # If a Bomb dies,
            # Nearby tiles and Bomb tile are Explosion (for 1 second)
            if bombLife >= 1:
                bombLife -= 1
                if bombLife == 0:
                    x, y = playerStats["x"], playerStats["y"]
                    explosionZone = [(x,y), (x-1,y), (x+1,y), (x,y-1), (x,y+1)]
                    map = copy.deepcopy(self.__agent.map)
                    for tile in explosionZone:
                        mapX, mapY = tile[0], tile[1]
                        if  mapY in range(len(map)) and mapX in range(len(map[mapY])) and map[mapY][mapX] == 1:
                            map[mapY][mapX] = 0
                    self.__agent.ruleArena("map", map)
                    for player, playerStats in self.__agent.range.items():
                        for tile in explosionZone:
                            if (playerStats["x"] == tile[0]) and (playerStats["y"] == tile[1]):
                                self.__agent.rulePlayer(player, "life", 0)

                # # If an Agent is a Bomb
                # # He automatically loses life
                self.__agent.rulePlayer(playerStats["clientId"], "life", bombLife)
        

    def doIfRangeChanged(self):
        ...

        for player, playerStats in self.__newRange.items():

            # Team points counter
            self.teamPointsCounter(playerStats)

            # If any agent starts shooting, he drops a bomb
            self.bombDrops(player, playerStats)

            # If a Bomb dies, nearby agents die / Bombs lose life
            self.bombExplodes(playerStats)

    def routine(self):
        while True:
            if self.__fsmState == "Initiating":

                # Initiate game
                self.initArena()

            if self.__fsmState == "inGame":

                # Startroutine
                self.startRoutine()

                # If range has changed
                if self.__oldRange != self.__newRange:
                    self.doIfRangeChanged()

                # Endroutine
                self.endRoutine()

referee =  Referee(playerId=ARBITRE_USERNAME, 
                      arena=ARENA, 
                      username=USERNAME, 
                      password=AGENT_PASSWORD, 
                      server=SERVER,
                      port = int(PORT),
                    )

referee.routine()