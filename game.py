import pygame
import random
from constants import *
from gameSystem import GameSystem
from chip import Chip
from plate import Plate

pygame.init()

SCREEN_X = 800
BOWL_LENGTH = SCREEN_X*0.5
BOWL_POSITION = SCREEN_X*0.25
PLATE_LENGTH = SCREEN_X*0.2
PLATE_HALF_POSITION = SCREEN_X*0.4
CHIP_LENGTH = SCREEN_X*0.05

my_font = pygame.font.SysFont('Ariel', 30)
screen = pygame.display.set_mode((SCREEN_X, SCREEN_X), pygame.HWSURFACE|pygame.DOUBLEBUF)
gameSystem = GameSystem()

chips = []
plates = []

# Create all plates (players score upon dropping a chip on a plate)
plateRect = pygame.Rect(0, PLATE_HALF_POSITION, PLATE_LENGTH, PLATE_LENGTH)
plates.append(Plate(plateRect, PLAYER_ONE))
plateRect = pygame.Rect(PLATE_HALF_POSITION, PLATE_HALF_POSITION*2, PLATE_LENGTH, PLATE_LENGTH)
plates.append(Plate(plateRect, PLAYER_TWO))
plateRect = pygame.Rect(PLATE_HALF_POSITION, 0, PLATE_LENGTH, PLATE_LENGTH)
plates.append(Plate(plateRect, PLAYER_THREE))
plateRect = pygame.Rect(PLATE_HALF_POSITION*2, PLATE_HALF_POSITION, PLATE_LENGTH, PLATE_LENGTH)
plates.append(Plate(plateRect, PLAYER_FOUR))

# Issa bowl
bowl = pygame.Rect(BOWL_POSITION, BOWL_POSITION, BOWL_LENGTH, BOWL_LENGTH)

# Game loop
running = True
while running:
  screen.fill((255, 255, 255))
  pygame.draw.rect(screen, (200, 200, 200), bowl)

  # Check for events (mouse clicks, closing window)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

    if event.type == pygame.MOUSEBUTTONDOWN:
      mousePos = pygame.mouse.get_pos()
      for c in chips:
        if c.rect.collidepoint(mousePos[0], mousePos[1]):
          c.state = STATE_CHIP_PICKED
          c.owner = PLAYER_ONE
          break

    if event.type == pygame.MOUSEBUTTONUP:
      mousePos = pygame.mouse.get_pos()
      for c in chips:
        if c.rect.collidepoint(mousePos[0], mousePos[1]):
          c.state = STATE_CHIP_AVAIL
          c.owner = PLAYER_NONE
          break

  # Spawn chips
  if gameSystem.attemptChipSpawn() == True:
    randomChipPosX = BOWL_POSITION + 0.01*random.randint(2, 88)*BOWL_LENGTH
    randomChipPosY = BOWL_POSITION + 0.01*random.randint(2, 88)*BOWL_LENGTH
    chipRect = pygame.Rect(
      randomChipPosX,
      randomChipPosY,
      CHIP_LENGTH, CHIP_LENGTH)

    chips.append(Chip(chipRect))
  
  # Draw plates and check for chips dropped on plate, if so handle chip and score
  for p in plates:
    pygame.draw.rect(screen, p.getColor(), p)

    for c in chips:
      if p.rect.colliderect(c.rect):
        p.state = STATE_PLATE_CAN_SCORE

        if c.state == STATE_CHIP_AVAIL:
          if c.type == CHIP_TYPE_BONUS:
            p.score += 3
          else: 
            p.score += 1
          chips.remove(c)
          gameSystem.currChips -= 1
          del c
        break

      else: 
        p.state = STATE_PLATE_WONT_SCORE

  # Draw chips and handle movement
  for c in chips:
    if (c.owner == PLAYER_ONE):
      mousePos = pygame.mouse.get_pos()

      c.rect = pygame.Rect(
      mousePos[0] - CHIP_LENGTH/2,
      mousePos[1] - CHIP_LENGTH/2,
      CHIP_LENGTH, CHIP_LENGTH)
    # if (c.owner == PLAYER_TWO):
    # if (c.owner == PLAYER_THREE):
    # if (c.owner == PLAYER_FOUR):
    pygame.draw.rect(screen, c.getColor(), c.rect)
  
  print("Chips: " + str(len(chips)))

  # Create score objects
  playerOneScore = my_font.render(str(plates[0].score), True, (0, 0, 0))
  playerTwoScore = my_font.render(str(plates[1].score), True, (0, 0, 0))
  playerThreeScore = my_font.render(str(plates[2].score), True, (0, 0, 0))
  playerFourScore = my_font.render(str(plates[3].score), True, (0, 0, 0))

  # Display score
  screen.blit(playerOneScore, (SCREEN_X*0.1, SCREEN_X*0.5))
  screen.blit(playerTwoScore, (SCREEN_X*0.5, SCREEN_X*0.9))
  screen.blit(playerThreeScore, (SCREEN_X*0.5, SCREEN_X*0.1))
  screen.blit(playerFourScore, (SCREEN_X*0.9, SCREEN_X*0.5))\

  # Update screen
  pygame.display.flip()

pygame.quit()