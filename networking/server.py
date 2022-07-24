# Connecting and sending sockets was developed by following this tutorial:
# https://levelup.gitconnected.com/learn-python-by-building-a-multi-user-group-chat-gui-application-af3fa1017689

import socket
import threading
import numpy as np

server = None
HOST_NAME = socket.gethostname()
HOST_ADDR = socket.gethostbyname(HOST_NAME)
HOST_PORT = 8080
client_name = " "
clients = []
clients_names = []
client_scores = []
MAX_CLIENTS = 5
idx = 0
chip_pos = np.random.rand(20, 2) * 500 # used for testing


def start_server():
    print("Your local IP address is:", HOST_ADDR,
          "Share this for people to join")
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST_ADDR, HOST_PORT))
        server.listen(MAX_CLIENTS)  # Max number of connects
        t = threading.Thread(target=accept_clients, args=(server,))
        t.start()
    except Exception as e:
        print("Error: unable to start thread", e)


def accept_clients(the_server):
    while True:
        client, addr = the_server.accept()
        clients.append(client)
        print(clients_names)
        # use a thread so as not to clog the gui thread
        t = threading.Thread(
            target=send_receive_client_message, args=(client, addr))
        t.start()
    # todo: have something to trigger to switching to listening mode and not accepting clients


def send_receive_client_message(client_connection, client_ip_addr):
    global idx

    # Get client name from clients
    client_name = client_connection.recv(4096)
    client_connection.send(str.encode("Connection Successful\n"))
    print(client_name.decode())

    # Send a welcome message
    message = "Welcome {}. Use 'exit' to quit\n".format(client_name.decode())
    client_connection.send(message.encode())

    # todo: trigger indicating start of game
    if (len(clients) == 5):
        for c in clients: 
            c.sendall(str.encode("chip_spawning_pos: " + str(chip_pos)))

    clients_names.append(client_name)
    print(clients_names)

    client_msg = ""
    inx = -1
    while True:       
        try:
            data = client_connection.recv(4096)
            client_msg = data.decode()

            if not data:
                break
            if data == b'exit':
                print("exit", client_connection)
                break
            else: # broadcast
                inx = get_client_index(clients, client_connection)
                sending_client_name = clients_names[idx]

                for c in clients:  
                    if c != client_connection: 
                        # this version is used for testing purposes to differenciate messages from server/other clients
                        c.sendall(("from other client(s) -> ").encode() + str.encode(client_msg))
                        #c.sendall(str.encode(client_msg)

        except Exception as e:
            print("Error: unable to receive message from client", e)


    # # find the client index then remove from both lists(client name list and connection list)
    idx = get_client_index(clients, client_connection)
    del clients_names[idx]
    del clients[idx]
    print("removing client:", idx)
    print("cur clienst:", clients_names)
    client_connection.close()


# Helper function to return the index of the current client in the list of clients
def get_client_index(client_list, curr_client):
    idx = 0
    for conn in client_list:
        if conn == curr_client:
            break
        idx = idx + 1

    return idx


# Helper function for converting positions of player/chip to string/numeric
def read_pos(str):
    str = str.split(",")
    return int(str[0], int(str[1]))


def make_pos(tuple):
    return str(tup[0] + "," + str(tup[1]))


def main():
    print("main")
    start_server()


main()
