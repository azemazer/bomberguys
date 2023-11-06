from typing import Any
from ...src.api.bomberguys import *
import pytest

agent = PytactXBomberGuy(
    playerID='Alexandre',
    arena='creativecda2324',
    username="demo",
    password=input("🔑 password: "),
    server="mqtt.jusdeliens.com",
    verbosity=3
)
    
def test_update():
    ...

def test_move():
    ...

def test_setColor():
    ...

def test_dropBomb():
    ...
