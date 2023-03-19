import os
import time
from datetime import datetime, timedelta
from unittest import TestCase

import Macros
from Application import Application


class TestApplication(TestCase):
    """Application test class"""
    def test_validate_name(self):
        assert Application.validate_name("Jan Brzechwa")
        assert Application.validate_name("Wiesław Ślimak")

    def test_validate_name_fail(self):
        assert not Application.validate_name("Jan")
        assert not Application.validate_name("Jan ")
        assert not Application.validate_name("J21 B54")

    def test_validate_filename(self):
        assert Application.validate_filename("plik")
        assert Application.validate_filename("_file-1")

    def test_validate_filename_fail(self):
        assert not Application.validate_filename("plik.exe")
        assert not Application.validate_filename(".plik")

    def test_check_if_entered_two_dates(self):
        assert Application.check_if_entered_two_dates("31.01.2002 38.11.2030")
        assert Application.check_if_entered_two_dates("3002 380")

    def test_check_if_entered_two_dates_fail(self):
        assert not Application.check_if_entered_two_dates("31.01.200238.11.2030")
        assert not Application.check_if_entered_two_dates("31.01.200a 38.11.2030")
        assert not Application.check_if_entered_two_dates("31.01.2011  31.11.2030")
        assert not Application.check_if_entered_two_dates("31.01.2011 31.11.2030 15.11.2023")

    def test_validate_date(self):
        assert Application.validate_date("31.01.2002 18:30")
        assert Application.validate_date("1.1.2002 18:3")

    def test_validate_date_fail(self):
        assert not Application.validate_date("31-01-2002 18:30")
        assert not Application.validate_date("32.01.2002 18:30")
        assert not Application.validate_date("31.01.2002 25:30")
        assert not Application.validate_date("31.01.20 18:30")
        assert not Application.validate_date("32.012002.01 18:30")

    @staticmethod
    def app_for_database_tests(before_today, number_of_days):
        Macros.database_path = Macros.test_database_path
        app = Application(test=True)
        for i in range(-before_today, number_of_days - before_today):
            date = (datetime.now() + timedelta(days=i)).strftime(Macros.datetime_format)
            app._db.insert("Jan Brzechwa", date, date)
        return app

    def test_validate_number_of_reservations(self):
        app = self.app_for_database_tests(-1, Macros.max_reservations_num)
        try:
            assert app._validate_number_of_reservations("Jan Brzechwa")
            os.remove(Macros.test_database_path)
        except AssertionError as e:
            os.remove(Macros.test_database_path)
            raise e

    def test_validate_number_of_reservations_with_past(self):
        app = self.app_for_database_tests(1, Macros.max_reservations_num + 2)
        try:
            assert app._validate_number_of_reservations("Jan Brzechwa")
            os.remove(Macros.test_database_path)
        except AssertionError as e:
            os.remove(Macros.test_database_path)
            raise e

    def test_validate_number_of_reservations_fail(self):
        app = self.app_for_database_tests(-1, Macros.max_reservations_num + 1)
        try:
            assert not app._validate_number_of_reservations("Jan Brzechwa")
            os.remove(Macros.test_database_path)
        except AssertionError as e:
            os.remove(Macros.test_database_path)
            raise e

    def test_validate_number_of_reservations_current_day(self):
        app = self.app_for_database_tests(0, Macros.max_reservations_num + 1)
        try:
            assert app._validate_number_of_reservations("Jan Brzechwa")
            os.remove(Macros.test_database_path)
        except AssertionError as e:
            os.remove(Macros.test_database_path)
            raise e

    @staticmethod
    def app_for_database_tests2():
        Macros.database_path = Macros.test_database_path
        app = Application(test=True)
        date = datetime.now().replace(hour=12, minute=0)
        date_list = [date.strftime(Macros.datetime_format),
                     (date + timedelta(minutes=Macros.minute_interval)).strftime(Macros.datetime_format),
                     (date + timedelta(minutes=3 * Macros.minute_interval)).strftime(Macros.datetime_format),
                     (date + timedelta(minutes=4 * Macros.minute_interval)).strftime(Macros.datetime_format)]
        app._db.insert("Jan Brzechwa", date_list[0], date_list[1])
        app._db.insert("Jan Brzechwa", date_list[2], date_list[3])
        return app, date

    def test_check_if_date_is_available(self):
        app, date = self.app_for_database_tests2()
        try:
            assert app._check_if_date_is_available(date + timedelta(minutes=Macros.minute_interval))
            os.remove(Macros.test_database_path)
        except AssertionError as e:
            os.remove(Macros.test_database_path)
            raise e

    def test_check_if_date_is_available_fail(self):
        app, date = self.app_for_database_tests2()
        try:
            assert not app._check_if_date_is_available(date)
            start_hour = date.replace(hour=time.strptime(Macros.start_hour, Macros.time_format).tm_hour,
                                      minute=time.strptime(Macros.start_hour, Macros.time_format).tm_min)
            assert not app._check_if_date_is_available(start_hour - timedelta(minutes=1))
            end_hour = date.replace(hour=time.strptime(Macros.end_hour, Macros.time_format).tm_hour,
                                    minute=time.strptime(Macros.end_hour, Macros.time_format).tm_min)
            assert not app._check_if_date_is_available(end_hour - timedelta(minutes=Macros.minute_interval - 1))
            os.remove(Macros.test_database_path)
        except AssertionError as e:
            os.remove(Macros.test_database_path)
            raise e

    def test_open_and_close_time(self):
        open_time, close_time = Application.open_and_close_time(datetime.now())
        assert open_time.time() == datetime.strptime(Macros.start_hour, Macros.time_format).time()
        assert close_time.time() == datetime.strptime(Macros.end_hour, Macros.time_format).time()

    def test_find_new_hour(self):
        pass

    def test_get_name(self):
        pass

    def test_get_date(self):
        pass

    def test_find_available_periods(self):
        pass

    def test_get_duration(self):
        pass

    def test_make_reservation(self):
        pass

    def test_cancel_reservation(self):
        pass

    def test_get_time_interval(self):
        pass

    def test_print_schedule(self):
        pass

    def test_save_schedule(self):
        pass

    def test_get_sorted_reservations(self):
        pass

    def test_change_reservations_to_datetime(self):
        pass

    def test_change_reservations_to_string(self):
        pass

    def test_str(self):
        pass

    def test_create_csv(self):
        pass

    def test_create_json(self):
        pass
