import socket
import threading
import socket_code
from signal import signal, SIG_IGN
import pygame
from chip import Chip

# signal(SIG_IGN)

SCREEN_X = 800
CHIP_LENGTH = SCREEN_X * 0.05

# The network object sets up the client connection and listens
# to any messages from the server and sets the state changes in its attributes


class Network:
    def __init__(self, username, address, isHost=False):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = address
        self.port = 8080
        self.addr = (self.server, self.port)
        self.player = self.connect(username, address, isHost)
        self.currentPlayers = 0
        self.score = 0
        self.client_id = -1
        self.isHost = isHost
        self.isGameStart = False
        self.chips = []
        self.winner_id = -1
        self.gameEnded = False

    def operate_server_requests(self, instruction, data):
        print(instruction)

        if instruction == socket_code.CONNECTION_ACK:
            print("client - connection ack")
            self.client_id = data.replace(
                socket_code.CONNECTION_ACK, b'').decode()

        elif instruction == socket_code.START:
            self.isGameStart = True
            print("client - start game")

        elif instruction.startswith(socket_code.USER_COUNT):
            user_count = data.replace(socket_code.USER_COUNT, b'').decode()
            print("client - new user has joined: ", user_count)
            self.currentPlayers = user_count

        elif instruction.startswith(socket_code.SPAWN_CHIP):
            rawData = data.replace(socket_code.SPAWN_CHIP, b'')
            data = rawData.decode().split("?")
            location = data[0].split(",")
            type = data[1]
            id = int(data[2])

            # re-construct chip and put it in the network chip state
            chipRect = pygame.Rect(
                float(location[0]),
                float(location[1]),
                CHIP_LENGTH, CHIP_LENGTH)

            newChip = Chip(chipRect, id, type)
            self.chips.append(newChip)

            print(
                "Client: got broadcasted chip spawning pos from server ", float(location[0]), float(location[1]))

        elif instruction.startswith(socket_code.CHIP_POS_UPDATE):
            position = data.replace(socket_code.CHIP_POS_UPDATE, b'')
            data = position.decode().split("?")
            location = data[0].split(",")
            id = data[1]
            state = data[2]

            # Look for the chip and update its location and state
            for chip in self.chips:
                if (int(chip.id) == int(id)):
                    chip.state = state
                    chip.rect = pygame.Rect(
                        float(location[0]),
                        float(location[1]),
                        CHIP_LENGTH, CHIP_LENGTH)

        elif instruction.startswith(socket_code.ANNOUNCE_WINNER):
            print("The winning message is: ")
            print(data)
            self.winner_id = int(data.replace(
                socket_code.ANNOUNCE_WINNER, b'').decode())

        else:
            pass

    def receive_message_from_server(self, m):
        while True:
            from_server = self.client.recv(4096)

            if not from_server:
                break

            # first four bits are the instructions
            instruction = from_server[:4]
            data = from_server

            s = threading.Thread(
                target=self.operate_server_requests, args=(instruction, data))
            s.start()

            if(instruction == socket_code.ANNOUNCE_WINNER):
                print("TEST  aaaaaaaAAAAAAAAAAAAAAAA")
                self.gameEnded = True
                break

    def send_message_to_server(self, m):
        try:
            if (type(m) == str):
                self.client.send(m.encode())

            self.client.send(m)
        except Exception as e:
            print("Error: unable to send message to server in client thread", e)

    def start_message_thread(self, m):
        print(self.client)

        s = threading.Thread(
            target=self.send_message_to_server, args=(m))
        s.start()

    def connect_to_server(self, name):
        print("connecting to server ", self.server)
        try:
            self.client.connect((self.server, self.port))
            self.client.send(name.encode())  # Send username to server

            # create thread to receive messages from server
            t = threading.Thread(
                target=self.receive_message_from_server, args=("m"))
            t.start()

        except Exception as e:
            print("error connecting to server: ", e)

    def connect(self, username, address, isHost):
        self.server = address
        self.connect_to_server(username)

    def disconnect(self):
        self.client.close()
