import Macros
import time

from AlertType import AlertType
from ActionOption import ActionOption
from DataType import DataType


class Menu:
    def __init__(self):
        pass

    @staticmethod
    def main_menu():
        Macros.clear_screen()
        print("What do you want to do:",
              "1.Make a reservation",
              "2.Cancel a reservation",
              "3.Print schedule",
              "4.Save schedule to a file",
              "5.Exit", sep='\n')
        match input():
            case "1" | "Make a reservation":
                return ActionOption.Make
            case "2" | "Cancel a reservation":
                return ActionOption.Cancel
            case "3" | "Print schedule":
                return ActionOption.Print
            case "4" | "Save schedule to a file":
                return ActionOption.Save
            case "5" | "Exit":
                return ActionOption.Exit
        return None

    @staticmethod
    def gather_data(type):
        Macros.clear_screen()
        match type:
            case DataType.Name:
                print("What's your Name?")
            case DataType.Date:
                print("When would you like to book? {DD.MM.YYYY HH:MM}")
            case DataType.DateCancel:
                print("When is your reservation? {DD.MM.YYYY HH:MM}")
            case DataType.DaysToPrint:
                print("Please enter start and end date {DD.MM.YYYY DD.MM.YYYY} ")
        return input()

    @staticmethod
    def alert(alert_type):
        Macros.clear_screen()
        match alert_type:
            case AlertType.InvalidName:
                print("Given name is invalid, it should contain first name, last name and space between. "
                      "Only letters are valid")
            case AlertType.InvalidNumberOfReservation:
                print(f"User has more than {Macros.max_reservations_num} reservations already this week")
            case AlertType.InvalidDate:
                print("Entered invalid date format, it should be {DD.MM.YYYY HH:MM}")
            case AlertType.InvalidDateShort:
                print("Entered invalid date format, it should be {DD.MM.YYYY DD.MM.YYYY}")
            case AlertType.DayFull:
                print("Given day is full, enter new date")
            case AlertType.DateFromThePast:
                print(f"Entered past date, please select some in interval at {float(Macros.minute_delay/60)} hour{'s' if Macros.minute_delay/60 > 1 else ''}")
            case AlertType.DateTooClose:
                print(f"Entered too close date, please select some in interval at least {float(Macros.minute_delay/60)} hour{'s' if Macros.minute_delay/60 > 1 else ''}")
            case AlertType.NotANumber:
                print("Please enter a number")
            case AlertType.NumberOutOfRange:
                print("Number out of range")
            case AlertType.DateTooCloseToCancel:
                print("Cannot cancel reservation, date too close")
            case AlertType.CancelSuccessful:
                print("Successfully canceled")

        time.sleep(3)

    @staticmethod
    def unavailable_date(new_hour):
        Macros.clear_screen()
        print(
            f"The time you chose is unavailable, would you like to make a reservation for {new_hour} instead? (yes/no)")
        match input():
            case 'yes':
                return True
            case 'no':
                return False
        return None

    @staticmethod
    def gather_duration(periods):
        Macros.clear_screen()
        print("How long would you like to book court?")
        for i in range(1,periods+1):
            print(f"{i}) {i*Macros.minute_interval} minutes")
        return input()

    @staticmethod
    def success_message(name, date, period):
        Macros.clear_screen()
        print(f"Reservation successful: {name}, {date}, {period} minutes")
        time.sleep(3)

    @staticmethod
    def reservation_not_exist():
        Macros.clear_screen()
        print("Reservation doesnt exist, continue? (yes/no)")
        match input():
            case 'yes':
                return True
            case 'no':
                return False
        return None
