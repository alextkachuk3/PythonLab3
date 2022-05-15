import threading
import unittest

from client.metro_client import MetroClient
from server.metro_server import MetroServer
from test_config import db_host, db_port, db_user, db_password, db_name


class TestRemoteMetroSQL(unittest.TestCase):
    def init_server(self):
        self.server = MetroServer('127.0.0.1', 25565, db_host, db_port, db_user, db_password, db_name)
        self.th = threading.Thread(target=self.server.run)
        self.th.start()

    def close_server(self):
        self.server.metro.connection.cursor().execute("DROP TABLE metro_lines, metro_stations")
        self.client.close_server()
        self.th.join()

    def test_adding_lines(self):
        self.init_server()

        self.client = MetroClient('127.0.0.1', 25565)

        self.client.add_line('green')
        self.client.add_line('red')
        self.client.add_line('blue')

        result = self.server.metro.lines_list()
        self.close_server()

        self.assertEqual(result, [(1, 'green'), (2, 'red'), (3, 'blue')])

    def test_delete_lines(self):
        self.init_server()

        self.client = MetroClient('127.0.0.1', 25565)

        self.client.add_line('green')
        self.client.add_line('red')
        self.client.add_line('blue')
        self.client.delete_line(2)

        result = self.server.metro.lines_list()
        self.close_server()

        self.assertEqual(result, [(1, 'green'), (3, 'blue')])


if __name__ == '__main__':
    unittest.main()
