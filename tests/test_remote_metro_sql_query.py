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

        result = self.server.metro.get_lines_list()
        print(result)

        self.close_server()

        self.assertEqual(result, [(1, 'green'), (2, 'red'), (3, 'blue')])

    def test_delete_lines(self):
        self.init_server()

        self.client = MetroClient('127.0.0.1', 25565)

        self.client.add_line('green')
        self.client.add_line('red')
        self.client.add_line('blue')
        self.client.delete_line(2)

        result = self.server.metro.get_lines_list()
        print(result)

        self.close_server()

        self.assertEqual(result, [(1, 'green'), (3, 'blue')])

    def test_adding_stations(self):
        self.init_server()

        self.client = MetroClient('127.0.0.1', 25565)

        self.client.add_line('green')
        self.client.add_line('red')
        self.client.add_line('blue')
        self.client.add_station('Teremky', 3, '6:00:00', '23:45:00')
        self.client.add_station('Vystavkovyi Tsentr', 3, '6:00:00', '23:45:00')
        self.client.add_station('Vasylkivska', 3, '6:00:00', '23:45:00')
        self.client.add_station('Syrets', 1, '6:00:00', '23:40:00')
        self.client.add_station('Akademmistechko', 2, '6:00:00', '23:45:00')
        self.client.add_station('Holosiivska', 3, '6:30:00', '23:45:00')
        self.client.add_station('Dorohozhychi', 1, '6:00:00', '23:40:00')
        self.client.add_station('Lukianivska', 1, '6:00:00', '23:40:00')
        self.client.add_station('Sviatoshyn', 2, '6:00:00', '23:30:00')
        self.client.add_station('Nykvy', 2, '6:00:00', '23:45:00')
        self.client.add_station('Zoloti Vorota', 1, '6:00:00', '23:40:00')
        self.client.add_station('Demiivska', 3, '6:00:00', '23:45:00')
        result_stations = self.server.metro.stations_list()
        print(result_stations)

        self.close_server()

        self.assertEqual(result_stations,
                         [(1, 'Teremky', '6:00:00', '23:45:00', 3), (2, 'Vystavkovyi Tsentr', '6:00:00', '23:45:00', 3),
                          (3, 'Vasylkivska', '6:00:00', '23:45:00', 3), (4, 'Syrets', '6:00:00', '23:40:00', 1),
                          (5, 'Akademmistechko', '6:00:00', '23:45:00', 2),
                          (6, 'Holosiivska', '6:30:00', '23:45:00', 3), (7, 'Dorohozhychi', '6:00:00', '23:40:00', 1),
                          (8, 'Lukianivska', '6:00:00', '23:40:00', 1), (9, 'Sviatoshyn', '6:00:00', '23:30:00', 2),
                          (10, 'Nykvy', '6:00:00', '23:45:00', 2), (11, 'Zoloti Vorota', '6:00:00', '23:40:00', 1),
                          (12, 'Demiivska', '6:00:00', '23:45:00', 3)])

    def test_deleting_stations(self):
        self.init_server()

        self.client = MetroClient('127.0.0.1', 25565)

        self.client.add_line('green')
        self.client.add_line('red')
        self.client.add_line('blue')
        self.client.add_station('Teremky', 3, '6:00:00', '23:45:00')
        self.client.add_station('Vystavkovyi Tsentr', 3, '6:00:00', '23:45:00')
        self.client.add_station('Vasylkivska', 3, '6:00:00', '23:45:00')
        self.client.add_station('Syrets', 1, '6:00:00', '23:40:00')
        self.client.add_station('Akademmistechko', 2, '6:00:00', '23:45:00')
        self.client.add_station('Holosiivska', 3, '6:30:00', '23:45:00')
        self.client.add_station('Dorohozhychi', 1, '6:00:00', '23:40:00')
        self.client.add_station('Lukianivska', 1, '6:00:00', '23:40:00')
        self.client.add_station('Sviatoshyn', 2, '6:00:00', '23:30:00')
        self.client.add_station('Nykvy', 2, '6:00:00', '23:45:00')
        self.client.add_station('Zoloti Vorota', 1, '6:00:00', '23:40:00')
        self.client.add_station('Demiivska', 3, '6:00:00', '23:45:00')

        self.client.delete_station(3)
        self.client.delete_station(5)
        self.client.delete_station(9)
        self.client.delete_station(4)
        result_stations = self.server.metro.stations_list()
        print(result_stations)

        self.close_server()

        self.assertEqual(result_stations,
                         [(1, 'Teremky', '6:00:00', '23:45:00', 3), (2, 'Vystavkovyi Tsentr', '6:00:00', '23:45:00', 3),
                          (6, 'Holosiivska', '6:30:00', '23:45:00', 3), (7, 'Dorohozhychi', '6:00:00', '23:40:00', 1),
                          (8, 'Lukianivska', '6:00:00', '23:40:00', 1), (10, 'Nykvy', '6:00:00', '23:45:00', 2),
                          (11, 'Zoloti Vorota', '6:00:00', '23:40:00', 1), (12, 'Demiivska', '6:00:00', '23:45:00', 3)])

    def test_update_station(self):
        self.init_server()

        self.client = MetroClient('127.0.0.1', 25565)

        self.client.add_line('green')
        self.client.add_line('red')
        self.client.add_line('blue')
        self.client.add_station('Teremky', 3, '6:00:00', '23:45:00')
        self.client.add_station('Vystavkovyi Tsentr', 3, '6:00:00', '23:45:00')
        self.client.add_station('Vasylkovska', 3, '6:00:00', '23:45:00')
        self.client.add_station('Syrets', 1, '6:00:00', '23:40:00')
        self.client.add_station('Akademmistechko', 2, '6:00:00', '23:45:00')
        self.client.add_station('Holosivska', 3, '6:30:00', '23:45:00')
        self.client.add_station('Dorohozhychi', 1, '6:00:00', '23:40:00')

        self.client.update_station(3, 'Vasylkivska', '5:00:00', '23:00:00')
        self.client.update_station(6, 'Holosiivska', '5:30:00', '23:00:00')

        result = self.server.metro.stations_list()
        print(result)

        self.close_server()

        self.assertEqual(result,
                         [(1, 'Teremky', '6:00:00', '23:45:00', 3), (2, 'Vystavkovyi Tsentr', '6:00:00', '23:45:00', 3),
                          (3, 'Vasylkivska', '5:00:00', '23:00:00', 3), (4, 'Syrets', '6:00:00', '23:40:00', 1),
                          (5, 'Akademmistechko', '6:00:00', '23:45:00', 2),
                          (6, 'Holosiivska', '5:30:00', '23:00:00', 3), (7, 'Dorohozhychi', '6:00:00', '23:40:00', 1)])

    def test_find_station_by_name(self):
        self.init_server()

        self.client = MetroClient('127.0.0.1', 25565)

        self.client.add_line('green')
        self.client.add_line('red')
        self.client.add_line('blue')
        self.client.add_station('Teremky', 3, '6:00:00', '23:45:00')
        self.client.add_station('Vystavkovyi Tsentr', 3, '6:00:00', '23:45:00')
        self.client.add_station('Vasylkivska', 3, '6:00:00', '23:45:00')
        self.client.add_station('Syrets', 1, '6:00:00', '23:40:00')
        self.client.add_station('Akademmistechko', 2, '6:00:00', '23:45:00')
        self.client.add_station('Holosiivska', 3, '6:30:00', '23:45:00')
        self.client.add_station('Dorohozhychi', 1, '6:00:00', '23:40:00')
        self.client.add_station('Lukianivska', 1, '6:00:00', '23:40:00')
        self.client.add_station('Sviatoshyn', 2, '6:00:00', '23:30:00')
        self.client.add_station('Nykvy', 2, '6:00:00', '23:45:00')
        self.client.add_station('Zoloti Vorota', 1, '6:00:00', '23:40:00')
        self.client.add_station('Demiivska', 3, '6:00:00', '23:45:00')

        result = self.client.find_station_by_name('Sviatoshyn')
        print(result)

        self.close_server()

        self.assertEqual(result, (9, 'Sviatoshyn', '6:00:00', '23:30:00', 2))

    def test_get_count_of_line_stations(self):
        self.init_server()

        self.client = MetroClient('127.0.0.1', 25565)

        self.client.add_line('green')
        self.client.add_line('red')
        self.client.add_line('blue')
        self.client.add_station('Teremky', 3, '6:00:00', '23:45:00')
        self.client.add_station('Vystavkovyi Tsentr', 3, '6:00:00', '23:45:00')
        self.client.add_station('Vasylkivska', 3, '6:00:00', '23:45:00')
        self.client.add_station('Syrets', 1, '6:00:00', '23:40:00')
        self.client.add_station('Akademmistechko', 2, '6:00:00', '23:45:00')
        self.client.add_station('Holosiivska', 3, '6:30:00', '23:45:00')
        self.client.add_station('Dorohozhychi', 1, '6:00:00', '23:40:00')
        self.client.add_station('Lukianivska', 1, '6:00:00', '23:40:00')
        self.client.add_station('Sviatoshyn', 2, '6:00:00', '23:30:00')
        self.client.add_station('Nykvy', 2, '6:00:00', '23:45:00')
        self.client.add_station('Zoloti Vorota', 1, '6:00:00', '23:40:00')
        self.client.add_station('Demiivska', 3, '6:00:00', '23:45:00')

        result = self.client.get_count_of_line_stations(3)
        print(result)

        self.close_server()

        self.assertEqual(result, 5)

    def test_get_list_of_line_stations(self):
        self.init_server()

        self.client = MetroClient('127.0.0.1', 25565)

        self.client.add_line('green')
        self.client.add_line('red')
        self.client.add_line('blue')
        self.client.add_station('Teremky', 3, '6:00:00', '23:45:00')
        self.client.add_station('Vystavkovyi Tsentr', 3, '6:00:00', '23:45:00')
        self.client.add_station('Vasylkivska', 3, '6:00:00', '23:45:00')
        self.client.add_station('Syrets', 1, '6:00:00', '23:40:00')
        self.client.add_station('Akademmistechko', 2, '6:00:00', '23:45:00')
        self.client.add_station('Holosiivska', 3, '6:30:00', '23:45:00')
        self.client.add_station('Dorohozhychi', 1, '6:00:00', '23:40:00')
        self.client.add_station('Lukianivska', 1, '6:00:00', '23:40:00')
        self.client.add_station('Sviatoshyn', 2, '6:00:00', '23:30:00')
        self.client.add_station('Nykvy', 2, '6:00:00', '23:45:00')
        self.client.add_station('Zoloti Vorota', 1, '6:00:00', '23:40:00')
        self.client.add_station('Demiivska', 3, '6:00:00', '23:45:00')

        result_client = self.client.get_line_stations(3)
        result_server = self.server.metro.get_line_stations(3)
        print(result_server)

        self.close_server()

        self.assertEqual(result_client, result_server)

    def get_line_list(self):
        self.init_server()

        self.client = MetroClient('127.0.0.1', 25565)

        self.client.add_line('green')
        self.client.add_line('red')
        self.client.add_line('blue')
        self.client.add_station('Teremky', 3, '6:00:00', '23:45:00')
        self.client.add_station('Vystavkovyi Tsentr', 3, '6:00:00', '23:45:00')
        self.client.add_station('Vasylkivska', 3, '6:00:00', '23:45:00')
        self.client.add_station('Syrets', 1, '6:00:00', '23:40:00')
        self.client.add_station('Akademmistechko', 2, '6:00:00', '23:45:00')
        self.client.add_station('Holosiivska', 3, '6:30:00', '23:45:00')
        self.client.add_station('Dorohozhychi', 1, '6:00:00', '23:40:00')
        self.client.add_station('Lukianivska', 1, '6:00:00', '23:40:00')
        self.client.add_station('Sviatoshyn', 2, '6:00:00', '23:30:00')
        self.client.add_station('Nykvy', 2, '6:00:00', '23:45:00')
        self.client.add_station('Zoloti Vorota', 1, '6:00:00', '23:40:00')
        self.client.add_station('Demiivska', 3, '6:00:00', '23:45:00')

        result_client = self.client.get_lines_list()
        result_server = self.server.metro.get_lines_list()
        print(result_server)

        self.close_server()

        self.assertEqual(result_client, result_server)


if __name__ == '__main__':
    unittest.main()
