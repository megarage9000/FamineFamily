import socket
import threading
import socket_code

class Network: 
    def __init__(self, username, address):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = address
        self.port = 8080
        self.addr = (self.server, self.port)
        self.player = self.connect(username, address)

    def operate_server_requests(self, instruction):
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
    
    def receive_message_from_server(self, m):
        while True:
            from_server = self.client.recv(4096)

            if not from_server:
                break

            # first four bits are the instructions
            instruction = from_server[:4]
            self.operate_server_requests(instruction)
            print(instruction)

        self.client.close()

    def send_message_to_server(self, m):
        print(m)
        self.client.send(m)

    def start_message_thread(self, m):
        # Use this function in the game to send the strings to the server
        # TODO: message should be a bitstring
        print(self.client)

        s = threading.Thread(
            target = self.send_message_to_server, args=(m))
        s.start()

    def connect_to_server(self, name):
        print("connecting to server ", self.server)
        try:
            self.client.connect((self.server, self.port))
            self.client.send(name.encode())  # Send username to server

            # create thread to receive messages from server
            t = threading.Thread(
                target = self.receive_message_from_server, args=("m"))
            t.start()

        except Exception as e:
            print("error connecting to server: ", e)
    
    def connect(self, username, address):
        # todo - pass in username + client from ui
        self.server = address
        self.connect_to_server(username)




