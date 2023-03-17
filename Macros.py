import os


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


max_reservations_num = 2
database_path = "/Users/michal/Documents/sample.db"
datetime_format = '%d.%m.%Y %H:%M'
date_format = '%d.%m.%Y'
max_periods = 3
minute_interval = 30
start_hour = '9:30'
end_hour = '18:00'
time_format = '%H:%M'
minute_delay = 60
exit = ["exit", "Exit"]
