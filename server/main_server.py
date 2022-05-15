from server.metro_server import MetroServer

from config import db_host, db_port, db_user, db_password, db_name


def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':
    print_hi('Server')
    server = MetroServer('127.0.0.1', 25565, db_host, db_port, db_user, db_password, db_name)
    server.run()
