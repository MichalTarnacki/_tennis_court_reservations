import Macros
import time

from Enums import DataType, AlertType, ActionOption


class Menu:
    """Class separating UI from application"""
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
            case "5" | "Exit" | "exit":
                return ActionOption.Exit
        return None

    @staticmethod
    def get_data(alert_type, clear=True):
        if clear:
            Macros.clear_screen()
        match alert_type:
            case DataType.Name:
                print("What's your Name?")
            case DataType.Date:
                print("When would you like to book? {DD.MM.YYYY HH:MM}")
            case DataType.DateCancel:
                print("When is your reservation? {DD.MM.YYYY HH:MM}")
            case DataType.DaysToPrint:
                print("Please enter start and end date {DD.MM.YYYY DD.MM.YYYY} ")
            case DataType.FileFormat:
                print("Save as json or csv?")
            case DataType.FileName:
                print("Please enter a file name")
            case DataType.AnyInput:
                print("Enter any character to continue")
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
                print("Given day is full already, please enter new date")
            case AlertType.DateFromThePast:
                print(
                    f"Entered past date, please select some in gap at least {float(Macros.minute_delay / 60)} hour{'s' if Macros.minute_delay / 60 > 1 else ''}")
            case AlertType.DateTooClose:
                print(
                    f"Entered too close date, please select some in gap at least {float(Macros.minute_delay / 60)} hour{'s' if Macros.minute_delay / 60 > 1 else ''}")
            case AlertType.NotANumber:
                print("Please enter a number")
            case AlertType.NumberOutOfRange:
                print("Number out of range")
            case AlertType.DateTooCloseToCancel:
                print("Cannot cancel reservation, date too close")
            case AlertType.CancelSuccessful:
                print("Successfully canceled")
            case AlertType.FileAlreadyExists:
                print("File already exists, please select another name")
            case AlertType.FileAlreadyExists:
                print("Please enter one of following format")
            case AlertType.WrongDateOrder:
                print("End date is before start date")
            case AlertType.SaveSuccessful:
                print("Save successful")
        time.sleep(3)
        Macros.flush()

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
    def get_duration(periods):
        Macros.clear_screen()
        print("How long would you like to book court?")
        for i in range(1, periods + 1):
            print(f"{i}) {i * Macros.minute_interval} minutes")
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

    @staticmethod
    def print_schedule(app, start_date, end_date):
        Macros.clear_screen()
        print(app.__str__(start_date, end_date))
        Menu.get_data(DataType.AnyInput, clear=False)
