from constants import *

class Plate:
  def __init__(self, rect, owner):
    self.state = STATE_PLATE_WONT_SCORE
    self.rect = rect
    self.owner = owner
    self.score = 0

  def getColor(self):
    if self.owner == PLAYER_ONE:
      if self.state == STATE_PLATE_WONT_SCORE:
        return COLOR_PLATE_ONE_NORMAL
      else:
        return COLOR_PLATE_ONE_EAT

    elif self.owner == PLAYER_TWO:
      if self.state == STATE_PLATE_WONT_SCORE:
        return COLOR_PLATE_TWO_NORMAL
      else:
        return COLOR_PLATE_TWO_EAT

    elif self.owner == PLAYER_THREE:
      if self.state == STATE_PLATE_WONT_SCORE:
        return COLOR_PLATE_THREE_NORMAL
      else:
        return COLOR_PLATE_THREE_EAT
      
    elif self.owner == PLAYER_FOUR:
      if self.state == STATE_PLATE_WONT_SCORE:
        return COLOR_PLATE_FOUR_NORMAL
      else:
        return COLOR_PLATE_FOUR_EAT

