from client.metro_client import MetroClient


def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':
    print_hi('Client')
    client = MetroClient('127.0.0.1', 25565)
    client.add_line('Pink')
    print(client.get_lines_list())
    client.add_line('White')
    print(client.get_lines_list())
    print(client.get_line_stations(5))
