import csv
import os
import time
from datetime import datetime, timedelta

import Macros
from Database import Database
from Menu import Menu
from Enums import DataType, AlertType, ActionOption
import re
import json


class Application:
    """Class containing all of backend logic"""
    def __init__(self, test=False):
        self._db = Database(Macros.database_path)
        if not test:
            self.__loop()

    def __loop(self):
        while True:
            match Menu.main_menu():
                case ActionOption.Make:
                    self._make_reservation()
                case ActionOption.Cancel:
                    self._cancel_reservation()
                case ActionOption.Print:
                    self._print_schedule()
                case ActionOption.Save:
                    self._save_schedule()
                case ActionOption.Exit:
                    self._exit()
                    break

    @staticmethod
    def validate_name(name):
        return True if re.compile('^([A-Za-zęóąśłżźćńĘÓĄŚŁŻŹĆŃ]+\\s[A-Za-zęóąśłżźćńĘÓĄŚŁŻŹĆŃ]+)$').match(name) is not None else False

    @staticmethod
    def validate_filename(name):
        return True if re.compile('^[\\w\\-_]+$').match(name) is not None else False

    @staticmethod
    def check_if_entered_two_dates(date_string):
        return True if re.compile('^([0-9.]+\\s[0-9.]+)$').match(date_string) is not None else False

    @staticmethod
    def validate_date(date):
        try:
            datetime.strptime(date, Macros.datetime_format)
            return True
        except (Exception,):
            pass
        return False

    def _validate_number_of_reservations(self, name):
        reservations = self._db.fetch_all()
        reservations = self._change_reservations_to_datetime(reservations)
        reservations = list(filter(lambda x: datetime.now() < x[1], reservations))
        reservations = list(filter(lambda x: name == x[0], reservations))
        return False if reservations.__len__() > Macros.max_reservations_num else True

    def _check_if_date_is_available(self, date):
        dates = self._db.fetch_all()
        open_time, close_time = self.open_and_close_time(date)
        dates = self._change_reservations_to_datetime(dates)
        if close_time < date + timedelta(minutes=Macros.minute_interval) \
                or date < open_time:
            return

        for i in dates:
            if i[1] <= date < i[2] or i[1] < date + timedelta(minutes=Macros.minute_interval) < i[2]:
                return False
        return True

    @staticmethod
    def open_and_close_time(date):
        open_time = date.replace(minute=time.strptime(Macros.start_hour, Macros.time_format).tm_min,
                                 hour=time.strptime(Macros.start_hour, Macros.time_format).tm_hour,
                                 second=0, microsecond=0)
        close_time = date.replace(minute=time.strptime(Macros.end_hour, Macros.time_format).tm_min,
                                  hour=time.strptime(Macros.end_hour, Macros.time_format).tm_hour,
                                  second=0, microsecond=0)
        return open_time, close_time

    def _find_new_hour(self, date) -> None or datetime:
        date, close_time = self.open_and_close_time(date)
        while date + timedelta(minutes=Macros.minute_interval) < close_time:
            if date > datetime.now():
                if self._check_if_date_is_available(date):
                    return date
            date = date + timedelta(minutes=Macros.minute_interval)
        return None

    def _get_name(self, option):
        while True:  # Gather and valid name
            name = Menu.get_data(DataType.Name)
            if name in Macros.exit:
                return False
            elif self.validate_name(name):
                break
            else:
                Menu.alert(AlertType.InvalidName)
        if option == ActionOption.Make:
            if not self._validate_number_of_reservations(name):
                Menu.alert(AlertType.InvalidNumberOfReservation)
                return False
        return name

    def _get_date(self, option):
        while True:
            date = Menu.get_data(DataType.Date if option == ActionOption.Make else DataType.DateCancel)
            if date in Macros.exit:
                return False
            elif self.validate_date(date):
                date = datetime.strptime(date, Macros.datetime_format)
                if date < datetime.now():
                    Menu.alert(AlertType.DateFromThePast)
                elif option == ActionOption.Make:
                    if date < datetime.now() + timedelta(minutes=Macros.minute_delay):
                        Menu.alert(AlertType.DateTooClose)
                    elif self._check_if_date_is_available(date):
                        break
                    else:
                        date = self._find_new_hour(date)
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

    def _find_available_periods(self, date):
        available_periods = 1
        for i in range(1, Macros.max_periods):
            if self._check_if_date_is_available(date + timedelta(minutes=Macros.minute_interval * i)):
                available_periods += 1
            else:
                break
        return available_periods

    def _get_duration(self, date):
        periods = self._find_available_periods(date)
        while True:
            try:
                response = Menu.get_duration(periods)
                if response in Macros.exit:
                    return False
                response = int(response)
                if 1 <= response <= periods:
                    return response
                elif response in [i * Macros.minute_interval for i in range(1, Macros.max_periods + 1)]:
                    return response / Macros.minute_interval
                else:
                    Menu.alert(AlertType.NumberOutOfRange)
            except (Exception,):
                Menu.alert(AlertType.NotANumber)

    def _make_reservation(self):
        name = self._get_name(ActionOption.Make)
        if not name:
            return
        date = self._get_date(ActionOption.Make)
        if not date:
            return
        duration = self._get_duration(date)
        if not duration:
            return
        start_date = datetime.strftime(date, Macros.datetime_format)
        end_date = datetime.strftime(date + timedelta(minutes=duration * Macros.minute_interval),
                                     Macros.datetime_format)
        self._db.insert(name, start_date, end_date)
        Menu.success_message(name, date.strftime(Macros.datetime_format), int(duration * Macros.minute_interval))

    def _cancel_reservation(self):
        name = self._get_name(ActionOption.Cancel)
        if not name:
            return
        while True:
            date = self._get_date(ActionOption.Cancel)
            if not date:
                return
            date = date.strftime(Macros.datetime_format)
            if self._db.check_if_reservation_exists(name, date):
                self._db.cancel_reservation(name, date)
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

    def _get_time_interval(self):
        while True:
            next_days = Menu.get_data(DataType.DaysToPrint)
            if next_days in Macros.exit:
                return False
            elif self.check_if_entered_two_dates(next_days):
                start_date, end_date = next_days.split(" ")
                try:
                    start_date = datetime.strptime(start_date, Macros.date_format)
                    end_date = datetime.strptime(end_date, Macros.date_format)
                    if start_date <= end_date:
                        break
                    Menu.alert(AlertType.WrongDateOrder)
                except (Exception,):
                    Menu.alert(AlertType.InvalidDateShort)
            else:
                Menu.alert(AlertType.InvalidDateShort)
        return start_date, end_date

    def _print_schedule(self):
        interval = self._get_time_interval()
        if not interval:
            return
        start_date, end_date = interval
        Menu.print_schedule(self, start_date, end_date)

    def _save_schedule(self):
        interval = self._get_time_interval()
        if not interval:
            return
        start_date, end_date = interval
        while True:
            fformat = Menu.get_data(DataType.FileFormat)
            if fformat in Macros.exit:
                return
            elif fformat in ('CSV', 'csv', 'JSON', 'json'):
                break
            else:
                Menu.alert(AlertType.InvalidFormat)
        while True:
            name = Menu.get_data(DataType.FileName)
            if name in Macros.exit:
                return
            elif self.validate_filename(name):
                name = Macros.default_path + name
                if fformat.lower() == 'csv':
                    name += ".csv"
                    if os.path.isfile(name):
                        Menu.alert(AlertType.FileAlreadyExists)
                        continue
                    self._create_csv(start_date, end_date, name)
                else:
                    name += ".json"
                    if os.path.isfile(name):
                        Menu.alert(AlertType.FileAlreadyExists)
                        continue
                    self._create_json(start_date, end_date, name)
                Menu.alert(AlertType.SaveSuccessful)
                break

    def _exit(self):
        self._db.quit()

    def _get_sorted_reservations(self, start_date, end_date):
        reservations = self._db.fetch_all()
        reservations = self._change_reservations_to_datetime(reservations)
        reservations = list(filter(lambda x: start_date <= x[1] <= end_date, reservations))
        reservations.sort(key=lambda a: a[1])
        return reservations

    @staticmethod
    def _change_reservations_to_datetime(reservations):
        return [(i[0], datetime.strptime(i[1], Macros.datetime_format), datetime.strptime(i[2], Macros.datetime_format))
                for i in reservations]

    @staticmethod
    def _change_reservations_to_string(reservations):
        return [(i[0], datetime.strftime(i[1], Macros.datetime_format), datetime.strftime(i[2], Macros.datetime_format))
                for i in reservations]

    def __str__(self, start_date=datetime.now(), end_date=datetime.now() + timedelta(days=3)):
        to_print = ""
        reservations = self._get_sorted_reservations(start_date, end_date + timedelta(days=1))
        while True:
            if start_date.date() == datetime.now().date():
                to_print += "Today:\n"
            elif start_date.date() == datetime.now().date() + timedelta(days=1):
                to_print += "Tommorow:\n"
            elif start_date.date() < datetime.now().date() + timedelta(days=7):
                to_print += start_date.strftime("%A") + ":\n"
            else:
                to_print += start_date.strftime(Macros.date_format + " %A") + ":\n"
            found = False
            for i in reservations:
                if i[1].date() == start_date.date():
                    found = True
                    to_print += f"* {i[0]} {i[1].strftime(Macros.time_format)} - " \
                                f"{i[2].strftime(Macros.time_format)}\n"
            if not found:
                to_print += "No Reservations\n"
            to_print += '\n'
            if start_date == end_date:
                return to_print
            start_date = start_date + timedelta(days=1)

    def _create_csv(self, start_date, end_date, name):
        reservations = self._get_sorted_reservations(start_date, end_date + timedelta(days=1))
        reservations = self._change_reservations_to_string(reservations)
        fields = ['name', 'start_time', 'end_time']

        with open(name, 'w') as f:
            write = csv.writer(f)

            write.writerow(fields)
            write.writerows(reservations)

        f = open(name, "rt")
        data = f.read()
        data = data.replace(',', ', ')
        f.close()
        f = open(name, "wt")
        f.write(data)
        f.close()

    def _create_json(self, start_date, end_date, name):
        reservations = self._get_sorted_reservations(start_date, end_date + timedelta(days=1))
        to_json = {}
        while True:
            day_reservations = []
            for i in reservations:
                if i[1].date() == start_date.date():
                    day_reservations.append({"name": i[0], "start_time": i[1].strftime(Macros.time_format),
                                             "end_time": i[2].strftime(Macros.time_format)})
            to_json[start_date.strftime(Macros.weekdate_format)] = day_reservations
            if start_date == end_date:
                break
            start_date = start_date + timedelta(days=1)
        with open(name, "w") as f:
            json.dump(to_json, f, indent=1)
        pass
