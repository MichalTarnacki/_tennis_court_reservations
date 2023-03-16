import Macros
from MenuOption import MenuOption
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
            case "1", "Make a reservation":
                return MenuOption.Make
            case "2", "Cancel a reservation":
                return MenuOption.Cancel
            case "3", "Print schedule":
                return MenuOption.Print
            case "4", "Save schedule to a file":
                return MenuOption.Save
            case "5", "Exit":
                return MenuOption.Exit
    @staticmethod
    def gather_data():
        pass