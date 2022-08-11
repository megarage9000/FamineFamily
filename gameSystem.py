import random

class GameSystem:
  def __init__(self):
    self.maxChips = 15
    self.currChips = 0

  def attemptChipSpawn(self):
    if self.currChips < self.maxChips:
      spawnChance = random.randint(1,1000)
      # print("Spawn Chance: " + str(spawnChance))
      if spawnChance > 998 - (self.maxChips - self.currChips):
        self.currChips += 1
        return True
      else:
        return False
    else:
      return False

