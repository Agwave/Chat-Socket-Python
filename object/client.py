
import socket

class Client:
    def __init__(self, host="localhost", port="50007", transfer_type=socket.SOCK_STREAM):

        self.host = host
        self.port = port
        self.transfer_type = transfer_type

        self.socket = socket.socket(socket.AF_INET, self.transfer_type)
        self.socket.connect((self.host, self.port))

