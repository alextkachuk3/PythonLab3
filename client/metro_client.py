from socket import socket
from sys import getsizeof

from metro_request_enum import MetroRequest


class MetroClient:
    def __init__(self, host, port):
        self.client_socket = socket()
        self.host = host
        self.port = port

    def connect(self):
        self.client_socket.connect((self.host, self.port))

    def add_line(self, color: str):
        request = [MetroRequest.ADD_LINE.value, [color]]
        request = str(request).encode()
        self.connect()
        self.send_message_size(getsizeof(request))
        self.client_socket.send(request)

    def send_message_size(self, size):
        self.client_socket.send(str(size).encode())
        self.client_socket.recv(1)
