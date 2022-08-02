# Connecting and sending sockets was developed by following this tutorial:
# https://levelup.gitconnected.com/learn-python-by-building-a-multi-user-group-chat-gui-application-af3fa1017689

import socket
import threading
import socket_code
from enum import Enum


class Game_State(Enum):
    WAITING_FOR_START = 1,
    START = 2,
    END = 3,


game_state_lock = threading.Lock()
game_state = Game_State.WAITING_FOR_START
chips = []

HOST_NAME = socket.gethostname()
HOST_ADDR = socket.gethostbyname(HOST_NAME)
HOST_PORT = 8080
clients = []
clients_names = []
MAX_CLIENTS = 4


def set_game_state(state):
    global game_state
    game_state_lock.acquire()
    game_state = state
    game_state_lock.release()


def check_game_state(state):
    global game_state
    game_state_lock.acquire()
    isState = game_state == state
    game_state_lock.release()
    return isState


def get_IP():
    return HOST_ADDR

def start_server():
    print("Your local IP address is:", HOST_ADDR,
          "\nShare this for people to join")
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST_ADDR, HOST_PORT))
        server.listen(MAX_CLIENTS)  # Max number of connects

        # thread to accept clients
        t = threading.Thread(
            target=accept_clients, args=(server,))
        t.start()

        # server loop
        while True:
            global game_state
            if (len(clients) == MAX_CLIENTS):
                # TODO: put broadcast here - might be a good idea to kill the accept_client thread
                print("REACHED MAX CLIENTS")

            if (check_game_state(Game_State.START)):
                # TODO: we can create threads to send stuff here - like chips
                print("Game has started")

    except Exception as e:
        print("Error: unable to start thread", e)


def accept_clients(the_server):
    try: 
        while True:
            client, addr = the_server.accept()
            clients.append(client)

            # each client has their own thread
            t = threading.Thread(
                target=client_thread, args=(client, addr,))
            t.start()
    except Exception as e: 
        print("Error: unable to accept client connection", e)


def client_thread(client_connection, client_ip_addr):
    try: 
        # Get client name from clients
        client_name = client_connection.recv(4096)

        t = threading.Thread(
            target=send_to, args=(client_connection, socket_code.CONNECTION_ACK))
        t.start()

        clients_names.append(client_name)

        # Client listening thread
        while True:
            data = client_connection.recv(4096)

            if not data:
                break

            # first four bits are the instructions
            instruction = data[:4]

            operate_client_requests(instruction)
    except Exception as e: 
        print("Error: unable to create client thread", e)

    # find the client index then remove from both lists(client name list and connection list)
    # TODO: POSSIBLE CONCURRENCY RACE CONDITION
    idx = get_client_index(clients, client_connection)
    del clients_names[idx]
    del clients[idx]
    print("removing client:", idx)
    print("cur clienst:", clients_names)
    client_connection.close()


def operate_client_requests(instruction):
    if instruction == socket_code.CONNECTION_REQ:
        # TODO add functions to operate when join happens
        print("USER SENT JOIN")
    elif instruction == socket_code.START:
        # TODO add start functions to operate when join happens
        set_game_state(Game_State.START)
        print("USER SENT START")
    elif instruction == socket_code.CHIP_STATE_UPDATE: 
        # TODO add function to broadcast state change to other players
        print("CHIP STATE CHANGED")
    elif instruction == socket_code.POS_UPDATE: 
        # TODO add function for moving chip when position updates 
        print("CHIP POSITION UPDATED")
    else:
        print("CODE NOT FOUND")


# when we call broadcast, we need to put it on its own thread so it doesn't block
def broadcast(client_connection, message):
    for c in clients: 
        if c != client_connection: 
            c.sendall(message)


def send_to(client_connection, message):
    client_connection.send(message)


def get_client_index(client_list, curr_client):
    # Helper function to return the index of the current client in the list of clients
    idx = 0
    for conn in client_list:
        if conn == curr_client:
            break
        idx = idx + 1

    return idx


# def main():
#     start_server()


# main()
