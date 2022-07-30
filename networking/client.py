
# Connecting and sending sockets was developed by following this tutorial:
# https://levelup.gitconnected.com/learn-python-by-building-a-multi-user-group-chat-gui-application-af3fa1017689

import socket
import threading
import socket_code

client = None
HOST_PORT = 8080


def connect():
    # todo - pass in username + client from ui
    username = input("Enter Username: ")
    client_ip = input("Enter IP address to connect to: ")
    connect_to_server(username, client_ip)


def connect_to_server(name, client_ip):
    global client
    try:
        client = socket.socket()
        client.connect((client_ip, HOST_PORT))
        client.send(name.encode())  # Send username to server

        # create thread to receive messages from server
        t = threading.Thread(
            target=receive_message_from_server, args=(client, "m"))
        t.start()

    except Exception as e:
        print("error", e)


def operate_server_requests(instruction):
    if instruction == socket_code.CONNECTION_ACK:
        # TODO add functions to operate when join happens
        print("CLIENT SUCCESS JOIN")
    elif instruction == socket_code.START:
        # TODO add start functions to operate when join happens
        print("SERVER - START")
    elif instruction == socket_code.SPAWN_CHIP: 
        # TODO add chip object when spawning happens
        print("SERVER SPAWNED CHIP")
    else:
        print("CODE NOT FOUND")


def receive_message_from_server(sck, m):
    while True:
        from_server = sck.recv(4096)

        if not from_server:
            break

        # first four bits are the instructions
        instruction = from_server[:4]
        operate_server_requests(instruction)
        print(instruction)

    sck.close()


def start_message_thread(message):
    # Use this function in the game to send the strings to the server
    # TODO: message should be a bitstring
    global client
    print(client)

    s = threading.Thread(
        target=send_message_to_server, args=(client, message))
    s.start()


def send_message_to_server(sck, m):
    print(m)
    sck.send(m)

def main():
    connect()


main()
