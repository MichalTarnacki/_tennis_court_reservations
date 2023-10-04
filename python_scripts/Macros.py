import os
import sys

try:
    from termios import tcflush, TCIFLUSH
except (Exception,):
    pass

try:
    from msvcrt import kbhit, getch
except (Exception,):
    pass


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def flush():
    try:
        while kbhit():
            getch()
    except (Exception,):
        pass
    try:
        tcflush(sys.stdin, TCIFLUSH)
    except (Exception,):
        pass


max_reservations_num = 2
database_path = "sample.db"
test_database_path = "test.db"
datetime_format = '%d.%m.%Y %H:%M'
date_format = '%d.%m.%Y'
weekdate_format = '%d.%m'
max_periods = 3
minute_interval = 30
start_hour = '9:30'
end_hour = '18:00'
time_format = '%H:%M'
minute_delay = 60
exit = ["exit", "Exit"]
default_path = ""
