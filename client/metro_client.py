from socket import socket
from sys import getsizeof

from metro_request_enum import MetroRequest

CONST_SIZE_OF_SIZE_REQUEST = 64


class MetroClient:
    def __init__(self, host, port):
        self.client_socket = socket()
        self.host = host
        self.port = port

    def connect(self):
        self.client_socket.connect((self.host, self.port))

    def send_request(self, request):
        request = str(request).encode()
        self.send_message_size(getsizeof(request))
        self.client_socket.send(request)
        self.client_socket.recv(1)

    def get_response(self):
        response_size = self.get_response_size()
        response = self.client_socket.recv(response_size).decode('utf-8')
        self.client_socket.send('1'.encode())
        return response

    def send_message_size(self, size):
        self.client_socket.send(str(size).encode())
        self.client_socket.recv(1)

    def get_response_size(self):
        size = self.client_socket.recv(CONST_SIZE_OF_SIZE_REQUEST)
        self.client_socket.send('1'.encode())
        return int(size.decode('utf-8'))

    def add_line(self, color: str):
        self.connect()
        request = [MetroRequest.ADD_LINE.value, [color]]
        self.send_request(request)
        self.disconnect()

    def line_list(self):
        self.connect()
        request = [MetroRequest.LIST_OF_LINES.value, []]
        self.send_request(request)
        response = self.get_response()
        self.disconnect()
        return response

    def disconnect(self):
        self.client_socket.close()
        self.client_socket = socket()
