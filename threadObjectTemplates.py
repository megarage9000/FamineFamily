import random
from constants import *

class ChipTemplate:
  def __init__(self, x, y, chipType):
    self.x = x
    self.y = y
    self.type = chipType
  
class ChipMoveTemplate:
  def __init__(self, x, y, player):
    self.x = x
    self.y = y
    self.owner = owner

class ChipScoreTemplate:
  def __init__(self, chip, value, player):
    self.chip = chip
    self.value = value
    self.player = player
  