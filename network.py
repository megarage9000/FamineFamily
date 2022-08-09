import socket
import threading
import socket_code
from signal import signal, SIGPIPE, SIG_IGN
import pygame

signal(SIGPIPE, SIG_IGN)


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

    def operate_server_requests(self, instruction, data):
        print("SERVER INS: ")
        print(instruction)
        if instruction == socket_code.CONNECTION_ACK:
            # TODO add functions to operate when join happens
            self.client_id = data.replace(
                socket_code.CONNECTION_ACK, b'').decode()
            print("CLIENT SUCCESS JOIN", id)

        elif instruction == socket_code.START:
            self.isGameStart = True
            print("SERVER - START")

        elif instruction.startswith(socket_code.USER_COUNT):
            user_count = data.replace(socket_code.USER_COUNT, b'')
            print("SERVER - USER JOIN", user_count)
            self.currentPlayers = user_count

        elif instruction == socket_code.SPAWN_CHIP:
            # TODO add chip object when spawning happens
            position = data.replace(socket_code.SPAWN_CHIP, b'')
            print("Client: got broadcasted chip spawning pos from server " + position.decode())

        elif instruction.startswith(socket_code.CLIENT_ID):
            self.client_id = instruction.replace(socket_code.CLIENT_ID, b'')

        elif instruction == socket_code.CHIP_POS_UPDATE:
            position = data.replace(socket_code.CHIP_POS_UPDATE, b'')
            # TODO handle chip pos on the client/ui side
            print("Client: got broadcasted chip pos from server " + position.decode())

        elif instruction.startswith(socket_code.CHIP_STATE_UPDATE):
            new_state = data.replace(socket_code.CHIP_STATE_UPDATE, b'')
            print("Client: got broadcasted chip state from server " +
                  new_state.decode())

        elif instruction.startswith(socket_code.ANNOUNCE_WINNER):
            winner_id = data.replace(socket_code.ANNOUNCE_WINNER, b'')
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
            self.operate_server_requests(instruction, data)
            print("Client: message received from server", data.decode())

        # self.client.close()

    def send_message_to_server(self, m):
        print(m)
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

    def connect(self, username, address, isHost):
        # todo - pass in username + client from ui
        self.server = address
        self.connect_to_server(username)

    def disconnect(self):
        self.client.close()
