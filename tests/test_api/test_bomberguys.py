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
from typing import Any
from src.api.bomberguys import *
import src.api.j2l
import pytest


def createAgent():
    agent = PytactXBomberGuy(
        playerID='Alexandre',
        arena='bomberguys',
        username="demo",
        password=AGENT_PASSWORD,
        server="mqtt.jusdeliens.com",
        verbosity=3
    )
    return agent

def test_has_connected():
    agent = createAgent()
    agent.update()

    assert(agent.getTile(agent.getX(), agent.getY()) != [])
    
# def test_update():
#     # agent = createAgent()
#     # agent.update()

def test_move():
    agent = createAgent()
    agent.update()
    x = agent.getX()
    y = agent.getY()
    agent.move(1, 0)
    agent.update()
    assert(
        x != agent.getX() and
        y == agent.getY() and
        x == agent.getX() - 1
    )

def test_setColor():
    agent = createAgent()
    oldColor = agent.getColor()
    if oldColor != [100, 100, 100]:
        agent.setColor(100, 100, 100)
    else:
        agent.setColor(255, 255, 255)
    agent.update()
    newColor = agent.getColor()
    assert (oldColor != newColor)
    ...

def test_dropBomb():
    agent = createAgent()
    agent.update()
    agent.dropBomb()
    agent.update()

    assert (agent.getTile(agent.getX(),agent.getY()) != [])
