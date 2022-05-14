import pymysql as pymysql


class Metro:
    def __init__(self, host, port, user, password, db_name):
        self.connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db_name
        )
        print('Successfully connected...')
        self.init_tables()

    def __del__(self):
        self.connection.close()
        print('Connection closed...')

    def get_tables_list(self):
        table_name_list = []
        with self.connection.cursor() as cursor:
            cursor.execute('SHOW TABLES')
            for x in cursor:
                table_name_list.append(x[0])
        return table_name_list

    def init_tables(self):
        with self.connection.cursor() as cursor:
            table_list = self.get_tables_list()

            if 'metro_lines' not in table_list:
                try:
                    create_metro_lines_table_query = "CREATE TABLE metro_lines(" \
                                                     "id INT AUTO_INCREMENT PRIMARY KEY, " \
                                                     "color VARCHAR(50));"
                    cursor.execute(create_metro_lines_table_query)
                    print("Metro lines table created successfully")
                except pymysql.err.OperationalError:
                    print('Metro lines table creating failed')
                finally:
                    self.connection.commit()

            if 'metro_stations' not in table_list:
                try:
                    create_metro_stations_table_query = "CREATE TABLE metro_stations(" \
                                                        "id INT AUTO_INCREMENT PRIMARY KEY, " \
                                                        "name VARCHAR(100), " \
                                                        "open TIME, " \
                                                        "close TIME, " \
                                                        "metro_line_id INT, " \
                                                        "FOREIGN KEY (metro_line_id) " \
                                                        "REFERENCES metro_lines(id) " \
                                                        "ON UPDATE CASCADE ON DELETE CASCADE);"
                    cursor.execute(create_metro_stations_table_query)
                    print("Metro stations table created successfully")
                except pymysql.err.OperationalError:
                    print('Metro stations table creating failed')
                finally:
                    self.connection.commit()

    def add_line(self, color: str):
        try:
            with self.connection.cursor() as cursor:
                insert_line_query = "INSERT INTO metro_lines (color) VALUES(%s)"
                insert_line_val = color
                cursor.execute(insert_line_query, insert_line_val)
        finally:
            self.connection.commit()

    def delete_line(self, id: int):
        try:
            with self.connection.cursor() as cursor:
                delete_line_query = "DELETE FROM metro_lines WHERE id=(%s)"
                delete_line_id = id
                cursor.execute(delete_line_query, delete_line_id)
        finally:
            self.connection.commit()

    def update_color(self, id: str, color: str):
        try:
            with self.connection.cursor() as cursor:
                update_line_color_query = "UPDATE metro_lines SET color = %s WHERE id = %s"
                update_line_color_val = (color, id)
                cursor.execute(update_line_color_query, update_line_color_val)
        finally:
            self.connection.commit()

    def add_station(self, name: str, line_id: int, open: str, close: str):
        try:
            with self.connection.cursor() as cursor:
                add_station_query = "INSERT INTO metro_stations (NAME, OPEN, CLOSE, METRO_LINE_ID)" \
                                    " VALUES (%s, %s, %s, %s) "
                add_station_val = (name, open, close, line_id)
                cursor.execute(add_station_query, add_station_val)
        finally:
            self.connection.commit()

    def delete_station(self, id):
        try:
            with self.connection.cursor() as cursor:
                delete_station_query = "DELETE FROM metro_stations WHERE id=(%s)"
                delete_station_val = id
                cursor.execute(delete_station_query, delete_station_val)
        finally:
            self.connection.commit()

    def stations_list(self, row_count=100):
        with self.connection.cursor() as cursor:
            select_station_list_query = "SELECT * FROM metro_stations LIMIT %s"
            select_station_list_val = row_count
            cursor.execute(select_station_list_query, select_station_list_val)
            stations = cursor.fetchall()

        result = []

        for station in stations:
            result.append((station[0], station[1], str(station[2]), str(station[3]), station[4]))

        return result

    def lines_list(self, row_count=100):
        with self.connection.cursor() as cursor:
            select_lines_list_query = "SELECT * FROM metro_lines LIMIT %s"
            select_lines_list_val = row_count
            cursor.execute(select_lines_list_query, select_lines_list_val)
            lines = cursor.fetchall()

        result = []

        for line in lines:
            result.append((line[0], line[1]))

        return result

    def find_station(self, station_name):
        with self.connection.cursor() as cursor:
            station_find_query = "SELECT * FROM metro_stations WHERE name = %s"
            station_find_val = station_name
            cursor.execute(station_find_query, station_find_val)
            station = cursor.fetchall()[0]
            return station[0], station[1], str(station[2]), str(station[3]), station[4]

    def find_line(self, line_id):
        with self.connection.cursor() as cursor:
            line_find_query = "SELECT * FROM metro_lines WHERE id = %s"
            line_find_val = line_id
            cursor.execute(line_find_query, line_find_val)
            line = cursor.fetchall()[0]
            return line[0], line[1]

    def count_of_stations_on_line(self, line_id):
        with self.connection.cursor() as cursor:
            station_count_query = "SELECT COUNT(*) AS stations_count FROM metro_stations WHERE metro_line_id = %s"
            station_count_val = line_id
            cursor.execute(station_count_query, station_count_val)
            return cursor.fetchall()[0][0]

    def update_station_name(self, station_id, new_station_name):
        try:
            with self.connection.cursor() as cursor:
                update_station_name_query = "UPDATE metro_stations SET name = %s WHERE id = %s"
                update_station_name_val = (new_station_name, station_id)
                cursor.execute(update_station_name_query, update_station_name_val)
        finally:
            self.connection.commit()

    def update_open_time(self, station_id, new_open_time):
        try:
            with self.connection.cursor() as cursor:
                update_open_time_query = "UPDATE metro_stations SET open = %s WHERE id = %s"
                update_open_time_val = (new_open_time, station_id)
                cursor.execute(update_open_time_query, update_open_time_val)
        finally:
            self.connection.commit()

    def update_close_time(self, station_id, new_close_time):
        try:
            with self.connection.cursor() as cursor:
                update_close_time_query = "UPDATE metro_stations SET close = %s WHERE id = %s"
                update_close_time_val = (new_close_time, station_id)
                cursor.execute(update_close_time_query, update_close_time_val)
        finally:
            self.connection.commit()

    def get_line_stations(self, line_id):
        with self.connection.cursor() as cursor:
            select_line_stations_list_query = "SELECT * FROM metro_stations WHERE metro_line_id = %s"
            select_line_stations_list_val = line_id
            cursor.execute(select_line_stations_list_query, select_line_stations_list_val)
            stations = cursor.fetchall()

        result = []

        for station in stations:
            result.append((station[0], station[1], str(station[2]), str(station[3]), station[4]))

        return result
