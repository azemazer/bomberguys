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

from typing import Any
from src.api.bomberguys import *
import src.api.j2l
import pytest


def createAgent():
    agent = PytactXBomberGuy(
        playerID='Alexandre',
        arena='bomberguys',
        username="demo",
        password="",
        server="mqtt.jusdeliens.com",
        verbosity=3
    )
    return agent

def test_has_connected():
    agent = createAgent()
    agent.update()
    assert(agent.map != [])
    
# def test_update():
#     # agent = createAgent()
#     # agent.update()

def test_move():
    agent = createAgent()
    agent.update()
    x = agent.x
    y = agent.y
    agent.move(1, 0)
    agent.update()
    assert(
        x != agent.x and
        y == agent.y and
        x == agent.x - 1
    )

def test_setColor():
    agent = createAgent()
    ...

def test_dropBomb():
    agent = createAgent()
    agent.update()
    agent.dropBomb()
    agent.update()
    assert (agent.map[agent.x[agent.y]])
