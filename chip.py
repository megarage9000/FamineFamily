import random
from constants import *

class Chip:
  def __init__(self, rect, chipType):
    self.state = STATE_CHIP_AVAIL
    self.rect = rect
    self.owner = PLAYER_NONE
    self.type = chipType

  def getColor(self):
    if self.type == CHIP_TYPE_NORMAL:
      if self.state == STATE_CHIP_AVAIL:
        return COLOR_AVAIL_NORMAL_CHIP
      elif self.state == STATE_CHIP_PICKED:
        return COLOR_CLICKED_NORMAL_CHIP
      elif self.state == STATE_CHIP_UNAVAIL:
        return COLOR_UNAVAIL_NORMAL_CHIP

    else:
      if self.state == STATE_CHIP_AVAIL:
        return COLOR_AVAIL_BONUS_CHIP
      elif self.state == STATE_CHIP_PICKED:
        return COLOR_CLICKED_BONUS_CHIP
      elif self.state == STATE_CHIP_UNAVAIL:
        return COLOR_UNAVAIL_BONUS_CHIP
  