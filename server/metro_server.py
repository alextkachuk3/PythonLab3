from socket import socket
from sys import getsizeof

from metro_request_enum import MetroRequest
from metro import Metro

CONST_SIZE_OF_SIZE_REQUEST = 64


def get_message_size(client_socket) -> int:
    size = int(client_socket.recv(CONST_SIZE_OF_SIZE_REQUEST).decode('utf-8'))
    send_success_message(client_socket)
    return size


def send_response_size(size, client_socket):
    client_socket.send(str(size).encode())
    client_socket.recv(1)


def send_success_message(client_socket):
    client_socket.send('1'.encode())


def send_response(response, client_socket):
    response = str(response).encode()
    send_response_size(getsizeof(response), client_socket)
    client_socket.send(response)
    client_socket.recv(1)


class MetroServer:
    def __init__(self, host, port, db_host, db_port, db_user, db_password, db_name):
        self.stop = False
        self.metro_socket = socket()
        self.metro_socket.bind((host, port))
        self.metro = Metro(db_host, db_port, db_user, db_password, db_name)

    def __del__(self):
        self.metro_socket.close()

    def run(self):
        self.metro_socket.listen()

        while self.stop is False:
            (client_socket, client_address) = self.metro_socket.accept()
            message_size = get_message_size(client_socket)
            request = client_socket.recv(message_size)
            request = eval(request.decode('utf-8'))
            request_enum = MetroRequest(request[0])
            request_data = request[1]
            match request_enum:
                case MetroRequest.ADD_LINE:
                    self.metro.add_line(request_data[0])
                    send_success_message(client_socket)
                case MetroRequest.DELETE_LINE:
                    self.metro.delete_line(request_data[0])
                    send_success_message(client_socket)
                case MetroRequest.ADD_STATION:
                    self.metro.add_station(request_data[0], request_data[1], request_data[2], request_data[3])
                    send_success_message(client_socket)
                case MetroRequest.DELETE_STATION:
                    self.metro.delete_station(request_data[0])
                    send_success_message(client_socket)
                case MetroRequest.UPDATE_STATION:
                    self.metro.update_station(request_data[0], request_data[1], request_data[2], request_data[3])
                    send_success_message(client_socket)
                case MetroRequest.FIND_STATION_BY_NAME:
                    response = self.metro.find_station(request_data[0])
                    send_success_message(client_socket)
                    send_response(response, client_socket)
                case MetroRequest.COUNT_OF_LINE_STATIONS:
                    response = self.metro.count_of_stations_on_line(request_data[0])
                    send_success_message(client_socket)
                    send_response(response, client_socket)
                case MetroRequest.LIST_OF_LINE_STATIONS:
                    response = self.metro.get_line_stations(request_data[0])
                    send_success_message(client_socket)
                    send_response(response, client_socket)
                case MetroRequest.LIST_OF_LINES:
                    response = self.metro.lines_list()
                    send_success_message(client_socket)
                    send_response(response, client_socket)
                case MetroRequest.CLOSE:
                    self.stop = True
                    send_success_message(client_socket)
                    send_response("Exit server", client_socket)
                    self.metro_socket.close()
            client_socket.close()

    # def process_request(self, request, client_socket):
