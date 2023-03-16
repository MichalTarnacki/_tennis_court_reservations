import time
from datetime import datetime, timedelta

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
        open_time = date.replace(minute=time.strptime(Macros.start_hour, Macros.time_format).tm_min,
                                 hour=time.strptime(Macros.start_hour, Macros.time_format).tm_hour)
        close_time = date.replace(minute=time.strptime(Macros.end_hour, Macros.time_format).tm_min,
                                  hour=time.strptime(Macros.end_hour, Macros.time_format).tm_hour)

        if close_time < date + timedelta(minutes=Macros.minute_interval) \
           or date < open_time:
            return

        for i in dates:
            if datetime.strptime(i[0], Macros.date_format) <= date < datetime.strptime(i[1], Macros.date_format) \
                    or datetime.strptime(i[0], Macros.date_format) < date + timedelta(minutes=Macros.minute_interval) \
                    < datetime.strptime(i[1], Macros.date_format):
                return False
        return True

    def __find_new_hour(self, date):
        if date.date() == datetime.now().date():
            date = date.replace(minute=datetime.now().minute,
                                hour=datetime.now().hour) + timedelta(minutes=Macros.minute_delay)
        else:
            date = date.replace(minute=time.strptime(Macros.start_hour, Macros.time_format).tm_min,
                                hour=time.strptime(Macros.start_hour, Macros.time_format).tm_hour)
        close_time = date.replace(minute=time.strptime(Macros.end_hour, Macros.time_format).tm_min,
                                  hour=time.strptime(Macros.end_hour, Macros.time_format).tm_hour)
        while date + timedelta(minutes=Macros.minute_interval) < close_time:
            if self.__check_if_date_is_available(date):
                return date
            date = date + timedelta(minutes=Macros.minute_interval)
        return None

    def __get_name(self):
        while True:  # Gather and valid name
            name = Menu.gather_data(DataType.Name)
            if self.__validate_name(name):
                break
            else:
                Menu.alert(AlertType.InvalidName)
        if not self.__validate_number_of_reservations(name):
            Menu.alert(AlertType.InvalidNumberOfReservation)
            return False
        return name

    def __get_date(self):
        while True:  # Gather and valid data
            date = Menu.gather_data(DataType.Date)
            if self.__validate_date(date):
                date = datetime.strptime(date, Macros.date_format)
                if date < datetime.now():
                    Menu.alert(AlertType.DateFromThePast)
                elif date < datetime.now() + timedelta(minutes=Macros.minute_delay):
                    Menu.alert(AlertType.DateTooClose)
                elif self.__check_if_date_is_available(date):
                    break
                else:
                    date = self.__find_new_hour(date)
                    if date is not None:
                        hour = datetime.strftime(date, '%H:%M')
                        while True:
                            response = Menu.unavailable_date(hour)
                            if response is not None:
                                break
                        if response:
                            break
                    else:
                        Menu.alert(AlertType.DayFull)
            else:
                Menu.alert(AlertType.InvalidDate)
        return date

    def __find_available_periods(self, date):
        available_periods = 1
        for i in (1, Macros.max_periods + 1):
            if self.__check_if_date_is_available(date + timedelta(minutes=Macros.minute_interval * i)):
                available_periods += 1
            else:
                break
        return available_periods

    def __get_duration(self, date):
        periods = self.__find_available_periods(date)
        while True:  # Gather and valid duration
            try:
                response = int(Menu.gather_duration(periods))
                if 1 <= response <= periods:
                    return response
                else:
                    Menu.alert(AlertType.NumberOutOfRange)
            except (Exception,):
                Menu.alert(AlertType.NotANumber)

    # TODO Ask if reservation should be on intervals
    def __make_reservation(self):
        name = self.__get_name()
        if not name:
            return
        date = self.__get_date()
        duration = self.__get_duration(date)
        start_date = datetime.strftime(date, Macros.date_format)
        end_date = datetime.strftime(date + timedelta(minutes=duration * Macros.minute_interval), Macros.date_format)
        self.__db.insert(name, start_date, end_date)

    def __cancel_reservation(self):
        self.__db.insert("jan blachowicz", "31.01.2002 18:30", "31.01.2002 19:00")
        self.__db.insert("jan blachowicz", "31.01.2002 19:00", "31.01.2002 19:30")
        self.__db.insert("jan blachowicz", "31.01.2002 19:30", "31.01.2002 20:00")
        pass

    def __print_schedule(self):
        self.__db.printAll()
        pass

    def __save_schedule(self):
        pass

    def __exit(self):
        pass
