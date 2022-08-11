import sys
import pygame
import random
import threading
from constants import *
from gameSystem import GameSystem
from chip import Chip
from plate import Plate
from Button import Button
from network import Network
from server import get_IP, start_server, check_game_state, Game_State
from time import sleep
import socket_code

pygame.init()

SCREEN_X = 800
BUTTON_LENGTH = SCREEN_X * 0.1
BUTTON_WIDTH = SCREEN_X * 0.15
BOWL_LENGTH = SCREEN_X * 0.5
BOWL_POSITION = SCREEN_X * 0.25
PLATE_LENGTH = SCREEN_X * 0.2
PLATE_HALF_POSITION = SCREEN_X * 0.4
CHIP_LENGTH = SCREEN_X * 0.05
MAX_SCORE = 10
RARE_CHIP_VALUE = 3
NORMAL_CHIP_VALUE = 1

my_font = pygame.font.SysFont('Ariel', 30)
screen = pygame.display.set_mode(
    (SCREEN_X, SCREEN_X), pygame.HWSURFACE | pygame.DOUBLEBUF)
gameSystem = GameSystem()

menuScreen = pygame.display.set_mode(
    (SCREEN_X, SCREEN_X), pygame.HWSURFACE | pygame.DOUBLEBUF)

chips = []
plates = []

# Create all plates (players score upon dropping a chip on a plate)
plateRect = pygame.Rect(0, PLATE_HALF_POSITION, PLATE_LENGTH, PLATE_LENGTH)
plates.append(Plate(plateRect, PLAYER_ONE))
plateRect = pygame.Rect(PLATE_HALF_POSITION,
                        PLATE_HALF_POSITION * 2, PLATE_LENGTH, PLATE_LENGTH)
plates.append(Plate(plateRect, PLAYER_TWO))
plateRect = pygame.Rect(PLATE_HALF_POSITION, 0, PLATE_LENGTH, PLATE_LENGTH)
plates.append(Plate(plateRect, PLAYER_THREE))
plateRect = pygame.Rect(PLATE_HALF_POSITION * 2,
                        PLATE_HALF_POSITION, PLATE_LENGTH, PLATE_LENGTH)
plates.append(Plate(plateRect, PLAYER_FOUR))

# Issa bowl
bowl = pygame.Rect(BOWL_POSITION, BOWL_POSITION, BOWL_LENGTH, BOWL_LENGTH)

# blank screen
menuBG = pygame.Rect(0, 0, SCREEN_X, SCREEN_X)

# the butt-ons deez nutz
startButton = pygame.Rect(BUTTON_WIDTH, BUTTON_WIDTH,
                          BUTTON_LENGTH, BUTTON_LENGTH)

# Game loop
playGame = False
mainMenu = True

# network connection


def connect(userName, address, isHost=False):
    global n
    n = Network(userName, address, isHost)
    return n


def mainMenu():
    global n

    while True:
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 255), menuBG)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = my_font.render("Main Menu", True, "#b68f40")
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
                    joinCreateRoomMenu()
                    # playGame()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

    n.disconnect()


def joinCreateRoomMenu():
    global n

    while True:
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 255), menuBG)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = my_font.render("Join/Create Game Room", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        JOIN_BUTTON = Button(image=pygame.image.load("assets/join.png"), pos=(400, 250), text_input="PLAY",
                             font=my_font, base_color="#d7fcd4", hovering_color="White")

        CREATE_BUTTON = Button(image=pygame.image.load("assets/createRoom.png"), pos=(400, 550), text_input="CREATE",
                               font=my_font, base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [JOIN_BUTTON, CREATE_BUTTON]:
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if JOIN_BUTTON.checkForInput(MENU_MOUSE_POS):
                    joinRoom()
                if CREATE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    createRoom()

        pygame.display.update()


def joinRoom():
    global n

    addr_font = pygame.font.Font(None, 32)
    addr_text = ''
    addr_rect = pygame.Rect(300, 400, 140, 32)
    colour = pygame.Color('white')
    addrActive = False

    name_font = pygame.font.Font(None, 32)
    name_text = ''
    name_rect = pygame.Rect(300, 250, 140, 32)
    nameActive = False

    while True:
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 255), menuBG)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = my_font.render("Join an Existing Room", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        INPUT_NAME_TEXT = my_font.render("Screen Name", True, "#b68f40")
        INPUT_NAME_RECT = INPUT_NAME_TEXT.get_rect(center=(400, 225))

        INPUT_ADDR_TEXT = my_font.render("IP Address", True, "#b68f40")
        INPUT_ADDR_RECT = INPUT_ADDR_TEXT.get_rect(center=(400, 375))

        ENTER_BUTTON = Button(image=pygame.image.load("assets/enter.png"), pos=(400, 550), text_input="JOIN",
                              font=my_font, base_color="#d7fcd4", hovering_color="White")

        BACK_BUTTON = Button(image=pygame.image.load("assets/back.png"), pos=(100, 100), text_input="",
                             font=my_font, base_color="#d7fcd4", hovering_color="White")

        for button in [ENTER_BUTTON, BACK_BUTTON]:
            button.update(screen)

        # TODO: Add buttons/text input
        addr_surface = addr_font.render(addr_text, True, (255, 255, 255))
        name_surface = name_font.render(name_text, True, (255, 255, 255))
        pygame.draw.rect(screen, colour, addr_rect, 2)
        pygame.draw.rect(screen, colour, name_rect, 2)
        screen.blit(addr_surface, (addr_rect.x + 5, addr_rect.y + 5))
        screen.blit(name_surface, (name_rect.x + 5, name_rect.y + 5))
        addr_rect.w = max(200, addr_surface.get_width() + 10)
        name_rect.w = max(200, name_surface.get_width() + 10)

        screen.blit(MENU_TEXT, MENU_RECT)
        screen.blit(INPUT_NAME_TEXT, INPUT_NAME_RECT)
        screen.blit(INPUT_ADDR_TEXT, INPUT_ADDR_RECT)

        # TODO: add events in the loop to check for user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if addr_rect.collidepoint(MENU_MOUSE_POS):
                    addrActive = True
                    nameActive = False
                elif name_rect.collidepoint(MENU_MOUSE_POS):
                    addrActive = False
                    nameActive = True
                elif ENTER_BUTTON.checkForInput(MENU_MOUSE_POS):
                    connect(name_text, addr_text, False)
                    joinedRoom(addr_text, name_text)
                elif BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                    joinCreateRoomMenu()
                else:
                    addrActive = False
                    nameActive = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # TODO: implement enter button function via server...?

                    connect(name_text, addr_text, False)
                    joinedRoom(addr_text, name_text)
                if event.key != pygame.K_RETURN:
                    if addrActive == True and nameActive == False:
                        if event.key == pygame.K_BACKSPACE:
                            addr_text = addr_text[:-1]
                        else:
                            addr_text += event.unicode
                    if nameActive == True and addrActive == False:
                        if event.key == pygame.K_BACKSPACE:
                            name_text = name_text[:-1]
                        else:
                            name_text += event.unicode

        pygame.display.update()


def joinedRoom(IPAddr, name):
    global n

    listFont = pygame.font.Font(None, 32)
    firstUser = name + " has joined.\n"
    userList = [firstUser, "Waiting for users..."]
    listText = "There are " + \
        str(len(userList) - 1) + " users logged in. Waiting for users..."
    userListRect = pygame.Rect(150, 300, 140, 32)
    colour = pygame.Color('white')

    while True:
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 255), menuBG)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = my_font.render("In Room: " + IPAddr, True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        BACK_BUTTON = Button(image=pygame.image.load("assets/back.png"), pos=(100, 100), text_input="",
                             font=my_font, base_color="#d7fcd4", hovering_color="White")

        BEGIN_BUTTON = Button(image=pygame.image.load("assets/begin.png"), pos=(400, 550), text_input="",
                              font=my_font, base_color="#d7fcd4", hovering_color="White")

        userSurface = listFont.render(listText, True, (255, 255, 255))
        pygame.draw.rect(screen, colour, userListRect, 2)
        screen.blit(userSurface, (userListRect.x + 5, userListRect.y + 5))
        userListRect.w = max(400, userSurface.get_width() + 10)

        BACK_BUTTON.update(screen)
        BEGIN_BUTTON.update(screen)
        screen.blit(MENU_TEXT, MENU_RECT)

        # one extra for the placeholder "Waiting for users..." string in List
        if int(n.currentPlayers) >= 5:
            listText = "You've reached max capacity. Click Start to begin."
        else:
            listText = "There are " + str(n.currentPlayers) + \
                " users logged in. Waiting for users..."

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if BEGIN_BUTTON.checkForInput(MENU_MOUSE_POS):
                    # TODO: start game, linked with server
                    n.send_message_to_server(
                        socket_code.START)
                elif BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                    joinCreateRoomMenu()

        if (n.isGameStart):
            playGame()

        pygame.display.update()


def createRoom():
    global n

    input_font = pygame.font.Font(None, 32)
    user_text = ''
    input_rect = pygame.Rect(300, 300, 140, 32)
    colour = pygame.Color('white')
    active = False

    while True:

        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 255), menuBG)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = my_font.render(
            "Create a New Game Session", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        LABEL_TEXT = my_font.render("Enter your name below:", True, "#b68f40")
        LABEL_RECT = LABEL_TEXT.get_rect(center=(400, 250))

        # TODO: Add buttons
        CREATE_BUTTON = Button(image=pygame.image.load("assets/enter.png"), pos=(400, 550), text_input="JOIN",
                               font=my_font, base_color="#d7fcd4", hovering_color="White")

        BACK_BUTTON = Button(image=pygame.image.load("assets/back.png"), pos=(100, 100), text_input="",
                             font=my_font, base_color="#d7fcd4", hovering_color="White")

        for button in [CREATE_BUTTON, BACK_BUTTON]:
            button.update(screen)

        text_surface = input_font.render(user_text, True, (255, 255, 255))
        pygame.draw.rect(screen, colour, input_rect, 2)
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        input_rect.w = max(200, text_surface.get_width() + 10)

        screen.blit(MENU_TEXT, MENU_RECT)
        screen.blit(LABEL_TEXT, LABEL_RECT)

        # TODO: add events in the loop to check for user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(MENU_MOUSE_POS):
                    active = True
                    print("Candice dik fit in yo mouf")
                if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                    joinCreateRoomMenu()
                if CREATE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    print("Deez Nuts: " + user_text)
                    IP = get_IP()  # TODO Display IP address
                    print(IP)

                    t = threading.Thread(
                        target=start_server)
                    t.start()

                    while (check_game_state(Game_State.SERVER_NOT_STARTED)):
                        pass

                    connect(user_text, IP, True)
                    joinedRoom(IP, user_text)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # TODO: implement enter button function via server...?
                    print("ligma nuts in this server: " + user_text)
                    IP = get_IP()  # TODO Display IP address
                    print(IP)

                    t = threading.Thread(
                        target=start_server)
                    t.start()

                    while (check_game_state(Game_State.SERVER_NOT_STARTED)):
                        pass
                    connect(user_text, IP, True)
                    joinedRoom(IP, user_text)
                if active == True and event.key != pygame.K_RETURN:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode

        pygame.display.update()


def chipSpawner():
    global n
    chipCounter = 0

    sleep(2)
    while (True):
        if gameSystem.attemptChipSpawn() == True:
          randomChipPosX = BOWL_POSITION + 0.01 * \
              random.randint(2, 88) * BOWL_LENGTH
          randomChipPosY = BOWL_POSITION + 0.01 * \
              random.randint(2, 88) * BOWL_LENGTH

          # send chip spawning location to the server
          pos_tuple = (randomChipPosX, randomChipPosY)

          superDoritoChance = random.randint(1, 100)
          if superDoritoChance > 80:
              type = CHIP_TYPE_BONUS
          else:
              type = CHIP_TYPE_NORMAL

          id = chipCounter
          chipCounter += 1

          n.send_message_to_server(
            socket_code.SPAWN_CHIP + make_pos(pos_tuple).encode() + "?".encode() + type.encode() + "?".encode() + str(id).encode() + "?".encode())
          sleep(0.25)


def playGame():
    global n
    chipSpawnerStarted = False
    mousePos = pygame.mouse.get_pos()

    gameIsRunning = True
    while gameIsRunning:
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (200, 200, 200), bowl)

        if (n.winner_id != -1):
            joinRoom()
            # print("game should end")

        # Check for events (mouse clicks, closing window)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                n.client.close()
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                for c in n.chips:
                    if c.rect.collidepoint(mousePos[0], mousePos[1]) and c.state == STATE_CHIP_AVAIL:
                        c.state = STATE_CHIP_PICKED
                        c.owner = PLAYER_ONE
                        # update chip position and state
                        print("Client: sending chip state update " + c.state)
                        n.send_message_to_server(socket_code.CHIP_POS_UPDATE + make_pos(
                            tuple([mousePos[0], mousePos[1]])).encode() + "?".encode() + str(c.id).encode() + "?".encode()
                            + c.state.encode() + "?".encode())
                        break

            if event.type == pygame.MOUSEBUTTONUP:
                mousePos = pygame.mouse.get_pos()
                for c in n.chips:
                    if c.rect.collidepoint(mousePos[0], mousePos[1]):
                        c.state = STATE_CHIP_AVAIL
                        c.owner = PLAYER_NONE
                        print("Client: sending chip state update " + c.state)
                        n.send_message_to_server(socket_code.CHIP_POS_UPDATE + make_pos(
                            tuple([mousePos[0], mousePos[1]])).encode() + "?".encode() + str(c.id).encode() + "?".encode()
                            + c.state.encode() + "?".encode())
                        break

        # Spawn chips
        if n.isHost and not chipSpawnerStarted:
            chipSpawnThread = threading.Thread(target=chipSpawner)
            chipSpawnThread.start()
            chipSpawnerStarted = True

        # Draw plates and check for chips dropped on plate, if so handle chip and score
        for p in plates:
            pygame.draw.rect(screen, p.getColor(), p)

            for c in n.chips:
                if p.rect.colliderect(c.rect):
                    p.state = STATE_PLATE_CAN_SCORE

                    if c.state == STATE_CHIP_AVAIL:
                        if c.type == CHIP_TYPE_BONUS:
                            p.score += RARE_CHIP_VALUE
                            # update score for each client
                            print("PLATE INDEX: " + str(plates.index(p)) + " | CLIENT ID: " + str(int(n.client_id)-1))
                            if plates.index(p) == int(n.client_id)-1:
                                n.score += RARE_CHIP_VALUE
                                print("CLIENT SCORE: " + str(n.score))
                        else:
                            p.score += NORMAL_CHIP_VALUE
                            print("PLATE INDEX: " + str(plates.index(p)) + " | CLIENT ID: " + str(int(n.client_id)-1))
                            if plates.index(p) == int(n.client_id)-1:
                                n.score += NORMAL_CHIP_VALUE
                                print("CLIENT SCORE: " + str(n.score))
                        n.chips.remove(c)
                        gameSystem.currChips -= 1
                        del c
                    break

                else:
                    p.state = STATE_PLATE_WONT_SCORE

            if n.score >= MAX_SCORE:
                # annouce winner to server
                print("Client: sending winning client ID")
                n.send_message_to_server(
                    socket_code.ANNOUNCE_WINNER + str(n.client_id).encode())
                print("GAME OVER! Player " + n.client_id + " has won!")
                # TODO need to handle connection to get winner from network
                gameIsRunning = False
                joinRoom()
                break

        # Draw chips and handle movement
        for c in n.chips:
            if (c.owner == PLAYER_ONE):
                mousePos = pygame.mouse.get_pos()

                posX = mousePos[0] - CHIP_LENGTH / 2
                posY = mousePos[1] - CHIP_LENGTH / 2

                c.rect = pygame.Rect(
                    posX,
                    posY,
                    CHIP_LENGTH, CHIP_LENGTH)

            # real-time avail chip pos
            if (c.owner == None or c.state == STATE_CHIP_PICKED):
                mousePos = pygame.mouse.get_pos()

                if c.rect.collidepoint(mousePos[0], mousePos[1]):
                    posX = mousePos[0] - CHIP_LENGTH / 2
                    posY = mousePos[1] - CHIP_LENGTH / 2

                    pos_tuple = tuple([posX, posY])
                    movement = pygame.mouse.get_rel()
                    # detect mouse movement, only send update if the mouse moves
                    if (movement != (0, 0)):
                        n.send_message_to_server(socket_code.CHIP_POS_UPDATE + make_pos(
                            pos_tuple).encode() + "?".encode() + str(c.id).encode() + "?".encode()
                            + c.state.encode() + "?".encode())

            # if (c.owner == PLAYER_TWO):
            # if (c.owner == PLAYER_THREE):
            # if (c.owner == PLAYER_FOUR):
            pygame.draw.rect(screen, c.getColor(), c.rect)

        # print("Chips: " + str(len(chips)))

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

# helper function for conversion between positions as a tuple and string
def read_pos(str):
    str = str.split(",")
    return (int(str[0]), int(str[1]))


def make_pos(tup):
    return (str(tup[0]) + "," + str(tup[1]))


def end_screen(endgame_text):
    running = True
    while running:
        # Fill background with white
        screen.fill((255, 255, 255))

        # End game text
        end_game_text = my_font.render(endgame_text, True, "#000000")
        end_game_rect = end_game_text.get_rect(center=(SCREEN_X/2, SCREEN_X/4))
        screen.blit(end_game_text, end_game_rect)

        # Button leave
        leave_pos = (SCREEN_X/4, SCREEN_X / 2)
        leave_text = my_font.render("Leave Game", True, "#000000")
        leave_rect = leave_text.get_rect(center=(leave_pos[0], leave_pos[1] + 100))
        screen.blit(leave_text, leave_rect)
        leave_button = Button(image=pygame.image.load("assets/quit-icon.png"),
                              pos=leave_pos,
                              text_input="",
                              font=my_font,
                              base_color="#000000",
                              hovering_color="white")

        leave_button.update(screen)

        # Button to go to main menu
        return_pos = (3 * SCREEN_X/4, SCREEN_X/2)
        return_text = my_font.render("Return to Start", True, "#000000")
        return_rect = return_text.get_rect(center=(return_pos[0], return_pos[1] + 100))
        screen.blit(return_text, return_rect)
        return_to_menu = Button(image=pygame.image.load("assets/enter.png"),
                              pos=return_pos,
                              text_input="",
                              font=my_font,
                              base_color="#000000",
                              hovering_color="white")

        return_to_menu.update(screen)

        mouse_pos = pygame.mouse.get_pos()

        # Checks if user clicked closed window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_to_menu.checkForInput(mouse_pos):
                    # TODO: Return to main menu here
                    print("Returning to menu...")
                elif leave_button.checkForInput(mouse_pos):
                    # TODO: End game here
                    print("Leaving game...")
                    running = False

        pygame.display.flip()

mainMenu()
pygame.quit()
sys.exit()
