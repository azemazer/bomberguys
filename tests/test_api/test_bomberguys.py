# Allow import without error 
# "relative import with no known parent package"
# In vscode, add .env file with PYTHONPATH="..." 
# with the same dir to allow intellisense
import os
import sys
__testsDir__ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
__libdir__ = os.path.dirname(__testsDir__)
sys.path.append(__libdir__)

__srcDir__ = os.path.join(__libdir__ , 'src', 'api')
sys.path.append(__srcDir__)

from dotenv import load_dotenv
load_dotenv()
AGENT_PASSWORD = os.getenv('__AGENT_PASSWORD__')
SERVER = os.getenv('__SERVER__')
PORT = os.getenv('__PORT__')
USERNAME = os.getenv('__USERNAME__')
ARENA = os.getenv('__ARENA__')
from typing import Any
from src.api.bomberguys import *
import src.api.j2l
import pytest


def createAgent():
    agent = PytactXBomberGuy(
        playerID='test',
        arena=ARENA,
        username=USERNAME,
        password=AGENT_PASSWORD,
        server=SERVER,
        port=int(PORT),
        verbosity=3
    )
    return agent

agent = createAgent()
agent.setColor(200, 200, 200)
agent.update()

def test_has_connected():
    global agent
    agent.update()
    assert(agent.getTile(agent.getX(), agent.getY()) != [])
    
# def test_update():
#     # global agent
#     # agent.update()

def test_move():
    global agent
    agent.update()
    x = agent.getX()
    y = agent.getY()
    print(x, 'old x')
    print(y, 'old y')
    agent.move(-1, 1)
    agent.update()
    print(agent.getX(), 'new x')
    print(agent.getY(), 'new y')

    assert(
        x != agent.getX() and
        y != agent.getY() and
        x == agent.getX() + 1
    )

def test_setColor():
    global agent
    oldColor = agent.getColor()
    if oldColor != (100, 100, 100):
        agent.setColor(100, 100, 100)
    else:
        agent.setColor(255, 255, 255)
    agent.update()
    newColor = agent.getColor()
    assert (oldColor != newColor)
    ...

def test_dropBomb():
    global agent    
    agent.update()
    agent.dropBomb()
    agent.update()

    assert (agent.getTile(agent.getX(),agent.getY()) != [])

# test_has_connected()
# test_move()
# test_setColor()
# test_dropBomb()