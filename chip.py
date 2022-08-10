import random
from constants import *

class Chip:
  counter = 0
  def __init__(self, rect):
    self.state = STATE_CHIP_AVAIL
    self.rect = rect
    self.owner = PLAYER_NONE
    self.id = Chip.counter
    Chip.counter += 1
    
    superDoritoChance = random.randint(1,100)
    if superDoritoChance > 80: 
      self.type = CHIP_TYPE_BONUS
    else:
      self.type = CHIP_TYPE_NORMAL

  def getColor(self):
    if self.type == CHIP_TYPE_NORMAL:
      if self.state == STATE_CHIP_AVAIL:
        return COLOR_AVAIL_NORMAL_CHIP
      elif self.state == STATE_CHIP_PICKED:
        return COLOR_CLICKED_NORMAL_CHIP

    else:
      if self.state == STATE_CHIP_AVAIL:
        return COLOR_AVAIL_BONUS_CHIP
      elif self.state == STATE_CHIP_PICKED:
        return COLOR_CLICKED_BONUS_CHIP
  