import sqlite3


class Database:
    """Class managing application database"""
    def __init__(self, path):
        self.__con = sqlite3.connect(path)
        self.__cur = self.__con.cursor()
        self._manage()

    def _manage(self):
        self.__cur.execute("CREATE TABLE IF NOT EXISTS reservations ("
                           "pname VARCHAR, "
                           "start_time TEXT, "
                           "end_time TEXT, "
                           "PRIMARY KEY(pname, start_time, end_time));")

    def count_reservations(self, name):
        self.__cur.execute('SELECT COUNT(*) FROM reservations '
                           f'WHERE pname = "{name}" '
                           'GROUP BY pname')
        result = self.__cur.fetchall()
        return result[0][0] if result != [] else 0

    def get_reservations_dates(self):
        self.__cur.execute('SELECT start_time, end_time FROM reservations')
        return self.__cur.fetchall()

    def insert(self, name, start_date, end_date):
        self.__cur.execute("INSERT INTO reservations (pname, start_time, end_time) "
                           f'VALUES ("{name}", "{start_date}", "{end_date}")')
        self.__con.commit()

    def fetch_all(self):
        self.__cur.execute('SELECT * FROM reservations ')
        return self.__cur.fetchall()

    def quit(self):
        self.__con.commit()
        self.__con.close()

    def check_if_reservation_exists(self, name, date):
        self.__cur.execute('SELECT * FROM reservations '
                           f'WHERE pname = "{name}" and start_time = "{date}"')
        result = self.__cur.fetchall()
        return True if result != [] else False

    def cancel_reservation(self, name, date):
        self.__cur.execute('DELETE FROM reservations '
                           f'WHERE pname = "{name}" and start_time = "{date}"')
        self.__con.commit()
