import j2l.pytactx.agent as pytactx
import os
import time

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

while ( len(arbitre.game) == 0 ):
    arbitre.lookAt((arbitre.dir+1)%4)
    arbitre.update()

def initArena():
    arbitre.ruleArena("reset", True)
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
        "lifeIni" : 100,
        "ammoIni" : 100,
        "invisible" : False,
        "invincible" : False,
        "infiniteAmmo" : False,
        "collision" : False,
                   }
    
    for ruleKey, ruleValue in bombRuleset.items():
        ruleActualValues = arbitre.game[ruleKey]
        ruleActualValues[1] = ruleValue
        arbitre.ruleArena(ruleKey, ruleActualValues)

    arbitre.update()

    agents =  {
        "joueur1": {
            "team": "0",
            "x": 3,
            "y": 3
        },
        "joueur2": {
            "team": "0",
            "x": 3,
            "y": 5
        },
        # "joueur3": {
        #     "team": "0",
        #     "x": 3,
        #     "y": 7
        # },
        "joueur4": {
            "team": "1",
            "x": 13,
            "y": 3
        },
        "joueur5": {
            "team": "1",
            "x": 13,
            "y": 5
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
    arbitre.update()

    exit()

    # "profiles" : { "?fr":"Liste des profiles de agents avec stats différentes", "ini":["default", "attaquant", "defenseur", "arbitre", "ball"], "publish":true },
    # "pIcons" : { "?fr":"Icone de chaque profiles de agents", "ini":["", "⚔️", "🛡️", "👀", ""], "publish":true },
    # "pImgs" : { "?fr":"Url des images de chaque profiles de agents. Chaine vide => dessin cercle", "ini":["ova.svg", "ova.svg", "ova.svg", "ova.svg", "ball.svg"], "publish":true },
    # "pPnj" : { "?fr":"Classe d'ia pour request auto. IA possibles '':desactiver ia, 'Idle':inoffensive, 'StaticTurret:tourne sur soi-même et tir, 'RandomMovingTurret':déplacement aléatoire et tir, 'SearchNDestroyBehaviour': agents dans metal gear solid 1", "ini":["","","","","Idle","SearchNDestroy"], "publish":false },
    # "range" : { "?fr":"Rayon de visibilite. En nb de cases. 0 pour tout voir.", "ini":[10,10,10,0,0], "min":0, "max":10, "publish":true },
    # "dtDir" : { "?fr":"Délai entre 2 changements d'orientation (en msecs)", "ini":[300,300,450,10,10], "min":0, "max":10000, "publish":true },
    # "dtMove" : { "?fr":"Délai entre 2 déplacements (en msecs)", "ini":[300,300,450,10,10], "min":0, "max":10000, "publish":true },
    # "dtFire" : { "?fr":"Délai entre 2 tirs (en msecs)", "ini":[300,300,300,0,0], "min":0, "max":10000, "publish":true },
    # "fxFire" : { "?fr":"Si oui ou non fonction tir possible", "ini":[true,true,true,true,false], "publish":true },
    # "hitFire" : { "?fr":"Dégats infligés par tir", "ini":[10,15,10,100,0], "min":0, "max":100, "publish":true },
    # "hitCollision" : { "?fr":"Dégats infligés par collision", "ini":[10,15,10,0,0], "min":0, "max":100, "publish":true },
    # "dxMax" : { "?fr":"Déplacement max autorisé en x", "ini":[1,1,1,100,1], "min":0, "max":10, "publish":true },
    # "dyMax" : { "?fr":"Déplacement max autorisé en y", "ini":[1,1,1,1,1,100,1], "min":0, "max":10, "publish":true },
    # "lifeIni" : { "?fr":"Nombre vie par agent", "ini":[100,75,150,0,0], "min":0, "max":100, "publish":true },
    # "ammoIni" : { "?fr":"Nombre munitions par agent", "ini":[100,100,100,0,0], "min":0, "max":100, "publish":true },
    # "invisible": { "?fr":"Si oui ou non invisible", "ini":[false,false,false,true,false], "publish":true },
    # "invincible": { "?fr":"Si oui ou non invincible", "ini":[false,false,false,true,true], "publish":true },
    # "infiniteAmmo": { "?fr":"Si oui ou non munitions infinies", "ini":[false,false,false,true,false], "publish":true },
    # "collision" : { "?fr":"Si oui ou non collision possible avec autres agents", "ini":[true,true,true,false,true], "publish":true }

initArena()

# Boucle principale pour actualiser l'arbitre 
while True:
    # Changement d'orientation de l'arbitre pour montrer qu'il est actif dans l'arène
    arbitre.lookAt((arbitre.dir+1)%4)
    arbitre.update()
    arbitre.ruleArena("info", "testest")