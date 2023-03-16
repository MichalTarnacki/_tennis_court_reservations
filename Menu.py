import Macros
import time

from AlertType import AlertType
from MenuOption import MenuOption
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
                return MenuOption.Make
            case "2" | "Cancel a reservation":
                return MenuOption.Cancel
            case "3" | "Print schedule":
                return MenuOption.Print
            case "4" | "Save schedule to a file":
                return MenuOption.Save
            case "5" | "Exit":
                return MenuOption.Exit
        return None

    @staticmethod
    def gather_data(type):
        Macros.clear_screen()
        match type:
            case DataType.Name:
                print("What's your Name?")
            case DataType.Date:
                print("When would you like to book? {DD.MM.YYYY HH:MM}1")
            case DataType.Duration:
                pass
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
        for i in range(1,periods):
            print(f"{i}) {i*Macros.intervals} minutes")
        return input()
