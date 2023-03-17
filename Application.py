import time
from datetime import datetime, timedelta

import Macros
from AlertType import AlertType
from Database import Database
from Menu import Menu
from ActionOption import ActionOption
from DataType import DataType
import re


class Application:
    def __init__(self):
        self.__db = Database(Macros.database_path)
        self.__loop()

    def __loop(self):
        while True:
            match Menu.main_menu():
                case ActionOption.Make:
                    self.__make_reservation()
                case ActionOption.Cancel:
                    self.__cancel_reservation()
                case ActionOption.Print:
                    self.__print_schedule()
                case ActionOption.Save:
                    self.__save_schedule()
                case ActionOption.Exit:
                    self.__exit()
                    break

    @staticmethod
    def __validate_name(name):
        return True if re.compile('^([A-Za-z]+\\s[A-Za-z]+)$').match(name) is not None else False

    @staticmethod
    def __validate_two_dates(date_string):
        return True if re.compile('^([0-9.]+\\s[0-9.]+)$').match(date_string) is not None else False
    @staticmethod
    def __validate_date(date):
        try:
            datetime.strptime(date, Macros.datetime_format)
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
            if datetime.strptime(i[0], Macros.datetime_format) <= date < datetime.strptime(i[1], Macros.datetime_format) \
                    or datetime.strptime(i[0], Macros.datetime_format) < date + timedelta(minutes=Macros.minute_interval) \
                    < datetime.strptime(i[1], Macros.datetime_format):
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

    def __get_name(self, option):
        while True:  # Gather and valid name
            name = Menu.gather_data(DataType.Name)
            if name in Macros.exit:
                return False
            elif self.__validate_name(name):
                break
            else:
                Menu.alert(AlertType.InvalidName)
        if option == ActionOption.Make:
            if not self.__validate_number_of_reservations(name):
                Menu.alert(AlertType.InvalidNumberOfReservation)
                return False
        return name

    def __get_date(self, option):
        while True:  # Gather and valid data
            date = Menu.gather_data(DataType.Date if option == ActionOption.Make else DataType.DateCancel)
            if date in Macros.exit:
                return False
            elif self.__validate_date(date):
                date = datetime.strptime(date, Macros.datetime_format)
                if date < datetime.now():
                    Menu.alert(AlertType.DateFromThePast)
                elif option == ActionOption.Make:
                    if date < datetime.now() + timedelta(minutes=Macros.minute_delay):
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
                    if date < datetime.now() + timedelta(minutes=Macros.minute_delay):
                        Menu.alert(AlertType.DateTooCloseToCancel)
                        return False
                    else:
                        break

            else:
                Menu.alert(AlertType.InvalidDate)
        return date

    def __find_available_periods(self, date):
        available_periods = 1
        for i in (0, Macros.max_periods):
            if self.__check_if_date_is_available(date + timedelta(minutes=Macros.minute_interval * i)):
                available_periods += 1
            else:
                break
        return available_periods

    def __get_duration(self, date):
        periods = self.__find_available_periods(date)
        while True:  # Gather and valid duration
            try:
                response = Menu.gather_duration(periods)
                if response in Macros.exit:
                    return False
                response = int(response)
                if 1 <= response <= periods:
                    return response
                elif response in [i*Macros.minute_interval for i in range(1, Macros.max_periods+1)]:
                    return response/Macros.minute_interval
                else:
                    Menu.alert(AlertType.NumberOutOfRange)
            except (Exception,):
                Menu.alert(AlertType.NotANumber)

    # TODO Ask if reservation should be on intervals
    def __make_reservation(self):
        name = self.__get_name(ActionOption.Make)
        if not name:
            return
        date = self.__get_date(ActionOption.Make)
        if not date:
            return
        duration = self.__get_duration(date)
        if not duration:
            return
        start_date = datetime.strftime(date, Macros.datetime_format)
        end_date = datetime.strftime(date + timedelta(minutes=duration * Macros.minute_interval), Macros.datetime_format)
        self.__db.insert(name, start_date, end_date)
        Menu.success_message(name, date.strftime(Macros.datetime_format), int(duration * Macros.minute_interval))

    def __cancel_reservation(self):
        name = self.__get_name(ActionOption.Cancel)
        if not name:
            return
        while True:
            date = self.__get_date(ActionOption.Cancel)
            if not date:
                return
            date = date.strftime(Macros.datetime_format)
            if self.__db.check_if_reservation_exists(name, date):
                self.__db.cancel_reservation(name, date)
                Menu.alert(AlertType.CancelSuccessful)
                return
            else:
                while True:
                    result = Menu.reservation_not_exist()
                    if result is not None:
                        if result:
                            break
                        else:
                            return

    def __print_schedule(self):
        while True:
            next_days = Menu.gather_data(DataType.DaysToPrint)
            if self.__validate_two_dates(next_days):
                start_date, end_date = next_days.split(" ")
                try:
                    start_date = datetime.strptime(start_date, Macros.date_format)
                    end_date = datetime.strptime(end_date, Macros.date_format)
                    break
                except (Exception,):
                    Menu.alert(AlertType.InvalidDateShort)
            else:
                Menu.alert(AlertType.InvalidDateShort)
        print(self.__str__(start_date, end_date))

    def __save_schedule(self):
        self.__db.printAll()
        time.sleep(3)
        pass

    def __exit(self):
        pass

    def __str__(self, start_date=datetime.now(), end_date=datetime.now() + timedelta(days=3)):
        to_print = ""
        reservations = self.__db.fetch_all()

        while True:
            if start_date == datetime.now():
                to_print += "Today:\n"
            elif start_date == datetime.now() + timedelta(days=1):
                to_print += "Tommorow:\n"
            else:
                to_print += start_date.strftime("%A") + ":\n"
            if start_date == end_date:
                return to_print
            start_date = start_date + timedelta(days=1)

