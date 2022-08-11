import socket
import threading
import socket_code
from signal import signal, SIGPIPE, SIG_IGN
import pygame
from chip import Chip

signal(SIGPIPE, SIG_IGN)

# todo decide where to put this
SCREEN_X = 800
CHIP_LENGTH = SCREEN_X * 0.05
chip_lock = threading.Lock()


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

    def operate_server_requests(self, instruction, data):
        print("SERVER INS: ")
        print(instruction)
        if instruction == socket_code.CONNECTION_ACK:
            # TODO add functions to operate when join happens
            self.client_id = data.replace(
                socket_code.CONNECTION_ACK, b'').decode()


        elif instruction == socket_code.START:
            self.isGameStart = True
            print("SERVER - START")

        elif instruction.startswith(socket_code.USER_COUNT):
            user_count = data.replace(socket_code.USER_COUNT, b'')
            print("SERVER - USER JOIN", user_count)
            self.currentPlayers = user_count

        elif instruction.startswith(socket_code.SPAWN_CHIP):
            rawData = data.replace(socket_code.SPAWN_CHIP, b'')
            data = rawData.decode().split("?")
            location = data[0].split(",")
            type = data[1]
            id = int(data[2])

            chipRect = pygame.Rect(
                float(location[0]),
                float(location[1]),
                CHIP_LENGTH, CHIP_LENGTH)

            newChip = Chip(chipRect, id, type)
            # chip_lock.acquire()
            self.chips.append(newChip)
            # chip_lock.release()

            print(
                "Client: got broadcasted chip spawning pos from server ", float(location[0]), float(location[1]))

        elif instruction.startswith(socket_code.CLIENT_ID):
            self.client_id = instruction.replace(socket_code.CLIENT_ID, b'')

        elif instruction.startswith(socket_code.CHIP_STATE_UPDATE):
            new_state = data.replace(socket_code.CHIP_STATE_UPDATE, b'')
            data = new_state.decode().split("?")
            state = data[0]
            id = data[1]

            for chip in self.chips:
                if (chip.id == id):
                    chip.state = state
            print("Client: got broadcasted chip state from server " +
                  state, "length: ", len(state))

        elif instruction.startswith(socket_code.CHIP_POS_UPDATE):
            position = data.replace(socket_code.CHIP_POS_UPDATE, b'')
            data = position.decode().split("?")
            location = data[0].split(",")
            id = data[1]
            state = data[2]

            for chip in self.chips:
                if (int(chip.id) == int(id)):
                    chip.state = state
                    chip.rect = pygame.Rect(
                        float(location[0]),
                        float(location[1]),
                        CHIP_LENGTH, CHIP_LENGTH)

        elif instruction.startswith(socket_code.ANNOUNCE_WINNER):
            self.winner_id = int(data.replace(socket_code.ANNOUNCE_WINNER, b'').decode())

            # TODO handle winner annoucement in ui

        else:
            # print("INSTRUCTION NOT FOUND")
            # print(instruction)
            pass

    def receive_message_from_server(self, m):
        while True:
            from_server = self.client.recv(4096)

            if not from_server:
                break

            # first four bits are the instructions
            instruction = from_server[:4]
            data = from_server
            # self.operate_server_requests(instruction, data)

            s = threading.Thread(
                target=self.operate_server_requests, args=(instruction, data))
            s.start()
            # print("Client: message received from server", data.decode())

        # self.client.close()

    def send_message_to_server(self, m):
        try:
            if (type(m) == str):
                self.client.send(m.encode())

            self.client.send(m)
        except Exception as e:
            print("Error: unable to send message to server in client thread", e)

    def start_message_thread(self, m):
        # Use this function in the game to send the strings to the server
        # TODO: message should be a bitstring
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
            # Bubble up error for proper error detection
            raise

    def connect(self, username, address, isHost):
        # todo - pass in username + client from ui
        self.server = address
        self.connect_to_server(username)

    def disconnect(self):
        self.client.close()
