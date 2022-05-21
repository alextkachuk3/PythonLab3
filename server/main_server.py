from server.metro_server import MetroServer

from config import db_host, db_port, db_user, db_password, db_name

if __name__ == '__main__':
    server = MetroServer('127.0.0.1', 25565, db_host, db_port, db_user, db_password, db_name)
    server.run()
