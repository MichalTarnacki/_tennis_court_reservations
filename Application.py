from datetime import datetime

import Macros
from AlertType import AlertType
from Database import Database
from Menu import Menu
from MenuOption import MenuOption
from DataType import DataType
import re


class Application:
    def __init__(self):
        self.__db = Database(Macros.database_path)
        self.__loop()

    def __loop(self):
        while True:
            match Menu.main_menu():
                case MenuOption.Make:
                    self.__make_reservation()
                case MenuOption.Cancel:
                    self.__cancel_reservation()
                case MenuOption.Print:
                    self.__print_schedule()
                case MenuOption.Save:
                    self.__save_schedule()
                case MenuOption.Exit:
                    self.__exit()
                    break

    @staticmethod
    def __validate_name(name):
        return True if re.compile('^([A-Za-z]+\\s[A-Za-z]+)$').match(name) is not None else False

    @staticmethod
    def __validate_date(date):
        try:
            datetime.strptime(date, Macros.date_format)
            return True
        except (Exception,):
            pass
        return False

    def __validate_number_of_reservations(self, name):
        return False if self.__db.count_reservations(name) > Macros.max_reservations_num else True

    def __check_if_date_is_available(self, date):
        dates = self.__db.gather_reservations_dates()
        new_date = datetime.strptime(date, Macros.date_format)
        for i in dates:
            if datetime.strptime(i[0], Macros.date_format) <= new_date < datetime.strptime(i[1], Macros.date_format):
                return False
        return True

    def __find_new_hour(self, date):
        dates = self.__db.gather_reservations_dates()
        dates = [i for i in dates if i[]]
        new_date = datetime.strptime(date, Macros.date_format)
        for i in dates:
            if datetime.strptime(i[0], Macros.date_format) <= new_date < datetime.strptime(i[1], Macros.date_format):
                return False
        return True
        pass

    def __make_reservation(self):
        while True:  # Gather and valid name
            name = Menu.gather_data(DataType.Name)
            if self.__validate_name(name):
                break
            else:
                Menu.alert(AlertType.InvalidName)
        if not self.__validate_number_of_reservations(name):
            Menu.alert(AlertType.InvalidNumberOfReservation)
            return
        while True: # Gather and valid data
            date = Menu.gather_data(DataType.Date)
            if self.__validate_date(date):
                if self.__check_if_date_is_available(date):
                    pass
                else:
                    new_date = self.__find_new_hour(date)
                    hour = datetime.strptime(new_date, Macros.date_format).strftime('%H:%M')
                    while True:
                        response = Menu.unavailable_date(hour)
                        if response is not None:
                            break
                    if response:
                        date = new_date
                        break
            else:
                Menu.alert(AlertType.InvalidDate)
        while True: # Gather and valid duration
            duration =
    def __cancel_reservation(self):
        self.__db.insert("jan blachowicz", "31.01.2002 18:30", "31.01.2002 19:00")
        self.__db.insert("jan blachowicz", "31.01.2002 19:00", "31.01.2002 19:30")
        self.__db.insert("jan blachowicz", "31.01.2002 19:30", "31.01.2002 202:00")
        pass

    def __print_schedule(self):
        self.__db.printAll()
        pass

    def __save_schedule(self):
        pass

    def __exit(self):
        pass
