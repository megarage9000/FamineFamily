
# Connecting and sending sockets was developed by following this tutorial:
# https://levelup.gitconnected.com/learn-python-by-building-a-multi-user-group-chat-gui-application-af3fa1017689

import socket
import threading
import pygame

client = None
HOST_PORT = 8080

# game window for clients
width = 500
height = 500
# note: this is for initializing game window for clients
# win = pygame.display.set_mode((width, height))
# pygame.display.set_caption("client")

class Player():

    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = {x, y, width, height}

    def draw(self, win): 
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

def read_pos(str):
    str = str.split(",")
    return int(str[0], int(str[1]))


def make_pos(tuple):
    return str(tup[0] + "," + str(tup[1]))


def redraw(win, player):
    win.fill((255, 255, 255))
    player.draw(win)
    pygame.display.update()

#---------------------------------------------------------------------------------------------------------
# connection establishment

def connect():
    # todo - pass in username + client from ui
    username = input("Enter Username: ")
    client_ip = input("Enter IP address to connect to: ")
    connect_to_server(username, client_ip)


def connect_to_server(name, client_ip):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((client_ip, HOST_PORT))
        client.send(name.encode())  # Send username to server

        # create thread to receive messages from server
        t = threading.Thread(
            target=receive_message_from_server, args=(client, "m"))
        t.start()

        # create a thread to send messages
        s = threading.Thread(
            target=send_message_to_server, args=(client, "m"))
        s.start()  
    except Exception as e:
        print("error", e)


def send_message_to_server(sck, m):
    while True:
        message = input()
        sck.send(message.encode())


def receive_message_from_server(sck, m):
    while True:
        from_server = sck.recv(4096)
        if not from_server:
            break

        print("Server says: " + from_server.decode())

        if from_server.startswith(("chip_spawning_pos$").encode()):
            # todo: add actual game actions
            print("Chip positions received. ") 


    sck.close()


def main():
    connect()

    # note: this is for initializing players on screen
    # run = True
    # player = Player(50, 50, 100, 100, (255, 0, 0))

    # while run:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             run = False
    #             pygame.quit()

    #     redraw(win, player)


main()