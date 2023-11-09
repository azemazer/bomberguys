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

# Création de l'arbitre
arbitre = pytactx.Agent(playerId=ARBITRE_USERNAME, 
                      arena=ARENA, 
                      username=USERNAME, 
                      password=AGENT_PASSWORD, 
                      server=SERVER,
                      port = int(PORT),
                    )

oldRange = {}
newRange = {}

# while ( len(arbitre.game) == 0 ):
#     arbitre.lookAt((arbitre.dir+1)%4)
#     arbitre.update()

def bombExplode(x: int, y: int) -> None:
    
    # If an agent is on an explosion,
    # He dies

    # If a stone block is on an explosion,
    # It disappears

    explosionZone = [(x,y), (x-1,y), (x+1,y), (x,y-1), (x,y+1)]
    map = copy.deepcopy(arbitre.map)
    for tile in explosionZone:
        mapX, mapY = tile[0], tile[1]
        if  mapY in range(len(map)) and mapX in range(len(map[mapY])) and map[mapY][mapX] == 1:
            map[mapY][mapX] = 0
    arbitre.ruleArena("map", map)
    for player, playerStats in arbitre.range.items():
        for tile in explosionZone:
            if (playerStats["x"] == tile[0]) and (playerStats["y"] == tile[1]):
                arbitre.rulePlayer(player, "life", 0)
    

def initArena():
    """
    Function that executes at launch. Modifies the rules
    to implement bomb rules, 
    then spawns 6 agents 
    """

    #  Spawns random stoneblocks
    arbitre.ruleArena("mapImgs", [
                        "",
                        "stoneblock.jpg",
    ])

    arbitre.ruleArena("mapFriction", [
                        0.0,
                        1.0
    ])

    arbitre.ruleArena("mapRand", True)

    arbitre.ruleArena("mapRandFreq", 0.4)


    arbitre.ruleArena("reset", True)
    arbitre.update()

    time.sleep(5)
    arbitre.update()

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
        "lifeIni" : 10, # Is used for the bomb countdown.
        "ammoIni" : 0,
        "invisible" : False,
        "invincible" : False,
        "infiniteAmmo" : False,
        "collision" : True, # You can step over bombs.
        "nRespawn" : 1
                   }
    
    for ruleKey, ruleValue in bombRuleset.items():
        ruleActualValues = arbitre.game[ruleKey]
        ruleActualValues[1] = ruleValue
        arbitre.ruleArena(ruleKey, ruleActualValues)

    time.sleep(0.3)
    arbitre.update()

    dtFires = arbitre.game["dtFire"]
    infiniteAmmos = arbitre.game["infiniteAmmo"]
    nRespawns = arbitre.game["nRespawn"]
    # weaponss = arbitre.game["weapons"]
    dtFires[0] = 5000 # Bomb cooldown for default players
    infiniteAmmos[0] = False # Players don't have limited ammo so we can listen to their number of shoots
    nRespawns[0] = 1 # Players respawn only once
    # weaponss[0] = 0 # Players don't really "shoot"
    arbitre.ruleArena("dtFire", dtFires)
    arbitre.ruleArena("infiniteAmmo", infiniteAmmos)
    arbitre.ruleArena("nRespawn", nRespawns)
    # arbitre.ruleArena("weapons", weaponss)

    # Regular spawn of iron block
    # Positions of iron blocks (tuple of (x, y))

    arbitre.ruleArena("mapImgs", [
                        "",
                        "stoneblock.jpg",
                        "ironblock.jpg",
                        "hit.jpg"
    ])

    arbitre.ruleArena("mapFriction", [
                        0.0,
                        1.0,
                        1.0,
                        0.0
    ])

    arbitre.ruleArena("mapRand", False)

    arbitre.ruleArena("mapRandFreq", 0.0)

    time.sleep(0.3)
    arbitre.update()

    ironBlockPosX = (1, 3, 5, 7, 9, 11, 13)
    ironBlockPosY = (1, 3, 5, 7, 9)
    ironBlockPos = []
    for xPos in ironBlockPosX:
        for yPos in ironBlockPosY:
            ironBlockPos.append((xPos, yPos))

    print("yep we go through this")

    map = copy.deepcopy(arbitre.game["map"])
    for pos in ironBlockPos:
        mapX, mapY = pos[0], pos [1] 
        map[mapY][mapX] = 2

    arbitre.ruleArena("map", map)
    time.sleep(0.3)
    arbitre.update()

    agents =  {
        "joueur1": {
            "team": "0",
            "x": 2,
            "y": 2
        },
        "joueur2": {
            "team": "0",
            "x": 2,
            "y": 4
        },
        # "joueur3": {
        #     "team": "0",
        #     "x": 3,
        #     "y": 7
        # },
        "joueur4": {
            "team": "1",
            "x": 12,
            "y": 2
        },
        "joueur5": {
            "team": "1",
            "x": 12,
            "y": 4
        },
        # "joueur6": {
        #     "team": "1",
        #     "x": 13,
        #     "y": 7
        # },


    }

    for agentId, attributes in agents.items():
        for attributeKey, attributeValue in attributes.items():
            arbitre.rulePlayer(agentId, attributeKey, attributeValue)
    time.sleep(0.3)
    arbitre.update()

initArena()

# Boucle principale pour actualiser l'arbitre 
while True:
    # Changement d'orientation de l'arbitre pour montrer qu'il est actif dans l'arène
    arbitre.lookAt((arbitre.dir+1)%4)
    # arbitre.ruleArena("info", "testest")
    newRange = copy.deepcopy(arbitre.range)

    if oldRange != newRange:

        # Team points counters
        team0IsAlive = False
        team1IsAlive = False

        for player, playerStats in newRange.items():

            # If an agent die,
            # The other team wins a point
            if playerStats["team"] == 0:
                team0IsAlive = True
            if playerStats["team"] == 1:
                team1IsAlive = True

            # If any Agent starts shooting,
            # He drops a bomb
            if player in oldRange and oldRange[player]["nFire"] < playerStats["nFire"]:
                bombName = player + "b"
                if (bombName in newRange and newRange[bombName]["life"] <= 0) or (bombName not in newRange):
                    arbitre.rulePlayer(bombName, "profile", 1)
                    arbitre.rulePlayer(bombName, "x", playerStats["x"])
                    arbitre.rulePlayer(bombName, "y", playerStats["y"])
                    arbitre.rulePlayer(bombName, "life", 10)
            if playerStats["profile"] == 1:
                bombLife = playerStats["life"]
                # If a Bomb dies,
                # Nearby tiles and Bomb tile are Explosion (for 1 second)
                if bombLife >= 1:
                    bombLife -= 1
                    if bombLife == 0:
                        bombExplode(playerStats["x"], playerStats["y"])

                    # # If an Agent is a Bomb
                    # # He automatically loses life
                    arbitre.rulePlayer(playerStats["clientId"], "life", bombLife)
        
        infoScores = ""
        if team0IsAlive and team1IsAlive:
            infoScores = "Game: ongoing"
        elif not team0IsAlive and not team1IsAlive:
            infoScores = "GAME RESULT: DRAW!"
        elif team0IsAlive and not team1IsAlive:
            infoScores = "GAME RESULT: TEAM 1 WON!"
        elif not team0IsAlive and team1IsAlive:
            infoScores = "GAME RESULT: TEAM 2 WON!"
        arbitre.ruleArena("info", infoScores)
        

    oldRange = newRange
    arbitre.update()
    time.sleep(0.3)
    
    # If a team wins,
    # The game is paused  