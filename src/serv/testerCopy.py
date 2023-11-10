import j2l.pytactx.agent as pytactx
import os
import random

from dotenv import load_dotenv
load_dotenv()
AGENT_PASSWORD = os.getenv('__AGENT_PASSWORD__')
SERVER = os.getenv('__SERVER__')
PORT = os.getenv('__PORT__')
USERNAME = os.getenv('__USERNAME__')
ARENA = os.getenv('__ARENA__')
ARBITRE_USERNAME = os.getenv('__ARBITRE_USERNAME__')

agent = pytactx.Agent(playerId="joueur5", 
                      arena=ARENA, 
                      username=USERNAME, 
                      password=AGENT_PASSWORD, 
                      server=SERVER,
                      port = int(PORT),
                    )

while True:
    agent.move(random.randint(-1,0), random.randint(0,1))
    agent.fire(True)
    agent.update()