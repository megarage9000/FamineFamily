
# Connecting and sending sockets was developed by following this tutorial:
# https://levelup.gitconnected.com/learn-python-by-building-a-multi-user-group-chat-gui-application-af3fa1017689

import socket
import threading

client = None
HOST_PORT = 8080


def connect():
    # todo - pass in username + client from ui
    username = input("Enter Username: ")
    client_ip = input("Enter IP address to connect to: ")
    connect_to_server(username, client_ip)


def connect_to_server(name, client_ip):
    try:
        client = socket.socket()
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
        message = input("Message: ")
        sck.send(message.encode())


def receive_message_from_server(sck, m):
    while True:
        from_server = sck.recv(4096)
        if not from_server:
            break

        print("Server says: " + from_server.decode())

    sck.close()


def main():
    connect()


main()
