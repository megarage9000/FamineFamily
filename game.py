import sys, pygame
import random
from constants import *
from gameSystem import GameSystem
from chip import Chip
from plate import Plate
from Button import Button

pygame.init()

SCREEN_X = 800
BUTTON_LENGTH = SCREEN_X*0.1
BUTTON_WIDTH = SCREEN_X*0.15
BOWL_LENGTH = SCREEN_X*0.5
BOWL_POSITION = SCREEN_X*0.25
PLATE_LENGTH = SCREEN_X*0.2
PLATE_HALF_POSITION = SCREEN_X*0.4
CHIP_LENGTH = SCREEN_X*0.05
MAX_SCORE = 30
RARE_CHIP_VALUE = 3
NORMAL_CHIP_VALUE = 1

my_font = pygame.font.SysFont('Ariel', 30)
screen = pygame.display.set_mode((SCREEN_X, SCREEN_X), pygame.HWSURFACE|pygame.DOUBLEBUF)
gameSystem = GameSystem()

menuScreen = pygame.display.set_mode((SCREEN_X, SCREEN_X), pygame.HWSURFACE|pygame.DOUBLEBUF)

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

# blank screen
menuBG = pygame.Rect(0, 0, SCREEN_X, SCREEN_X)

# the butt-ons deez nutz
startButton = pygame.Rect(BUTTON_WIDTH, BUTTON_WIDTH, BUTTON_LENGTH, BUTTON_LENGTH)

# Game loop
playGame = False
mainMenu = True


def mainMenu():
  while True:
      screen.fill((255, 255, 255))
      pygame.draw.rect(screen, (0, 0, 255), menuBG)

      MENU_MOUSE_POS = pygame.mouse.get_pos()

      MENU_TEXT = my_font.render("MAIN MENU", True, "#b68f40")
      MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

      PLAY_BUTTON = Button(image=pygame.image.load("assets/play.png"), pos=(400, 250), text_input="PLAY",
                           font=my_font, base_color="#d7fcd4", hovering_color="White")

      QUIT_BUTTON = Button(image=pygame.image.load("assets/stop.png"), pos=(400, 550), text_input="QUIT",
                           font=my_font, base_color="#d7fcd4", hovering_color="White")

      screen.blit(MENU_TEXT, MENU_RECT)

      for button in [PLAY_BUTTON, QUIT_BUTTON]:
        button.update(screen)

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
          if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
            playGame()
          # if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
          #   options()
          if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
            pygame.quit()
            sys.exit()

      pygame.display.update()

def playGame():
  gameIsRunning = True
  while gameIsRunning:
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (200, 200, 200), bowl)

    # Check for events (mouse clicks, closing window)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

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

    # Check for events (mouse clicks, closing window)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        gameIsRunning = False

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
      randomChipPosX = BOWL_POSITION + 0.01 * random.randint(2, 88) * BOWL_LENGTH
      randomChipPosY = BOWL_POSITION + 0.01 * random.randint(2, 88) * BOWL_LENGTH
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
              p.score += RARE_CHIP_VALUE
            else:
              p.score += NORMAL_CHIP_VALUE
            chips.remove(c)
            gameSystem.currChips -= 1
            del c
          break

        else:
          p.state = STATE_PLATE_WONT_SCORE
      
      if p.score >= MAX_SCORE:
        print("GAME OVER! Player " + str(plates.index(p)) + " has won!")
        gameIsRunning = False

    # Draw chips and handle movement
    for c in chips:
      if (c.owner == PLAYER_ONE):
        mousePos = pygame.mouse.get_pos()

        posX = mousePos[0] - CHIP_LENGTH / 2
        posY = mousePos[1] - CHIP_LENGTH / 2

        c.rect = pygame.Rect(
          posX,
          posY,
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
    screen.blit(playerOneScore, (SCREEN_X * 0.1, SCREEN_X * 0.5))
    screen.blit(playerTwoScore, (SCREEN_X * 0.5, SCREEN_X * 0.9))
    screen.blit(playerThreeScore, (SCREEN_X * 0.5, SCREEN_X * 0.1))
    screen.blit(playerFourScore, (SCREEN_X * 0.9, SCREEN_X * 0.5))
    # Update screen
    pygame.display.flip()

mainMenu()

pygame.quit()
sys.exit()