import threading
import unittest

from client.metro_client import MetroClient
from server.metro_server import MetroServer
from test_config import db_host, db_port, db_user, db_password, db_name


class TestRemoteMetroSQL(unittest.TestCase):
    def close_server(self):
        self.server.metro.connection.cursor().execute("DROP TABLE metro_lines, metro_stations")
        self.client.close_server()

    def test_adding_lines(self):
        self.server = MetroServer('127.0.0.1', 25565, db_host, db_port, db_user, db_password, db_name)
        th = threading.Thread(target=self.server.run)
        th.start()

        self.client = MetroClient('127.0.0.1', 25565)

        self.client.add_line('green')
        self.client.add_line('red')
        self.client.add_line('blue')

        result = self.server.metro.lines_list()
        self.close_server()
        th.join()

        self.assertEqual(result, [(1, 'green'), (2, 'red'), (3, 'blue')])


if __name__ == '__main__':
    unittest.main()
