from socket import socket

from metro_request_enum import MetroRequest
from metro import Metro

CONST_SIZE_OF_SIZE_REQUEST = 64


def get_message_size(client_socket) -> int:
    size = int(client_socket.recv(CONST_SIZE_OF_SIZE_REQUEST).decode('utf-8'))
    client_socket.send('1'.encode())
    return size


def sent_response_size(client_socket, size):
    client_socket.send(str(size))


class MetroServer:
    def __init__(self, host, port, db_host, db_port, db_user, db_password, db_name):
        self.metro_socket = socket()
        self.metro_socket.bind((host, port))
        self.metro = Metro(db_host, db_port, db_user, db_password, db_name)

    def run(self):
        self.metro_socket.listen()

        while True:
            (client_socket, client_address) = self.metro_socket.accept()
            message_size = get_message_size(client_socket)
            request = client_socket.recv(message_size)
            self.process_request(request)

    def process_request(self, request):
        request = eval(request.decode('utf-8'))
        request_enum = MetroRequest(request[0])
        request_data = request[1]
        match request_enum:
            case MetroRequest.ADD_LINE:
                self.metro.add_line(request_data[0])
            case MetroRequest.DELETE_LINE:
                self.metro.delete_line(request_data[0])
