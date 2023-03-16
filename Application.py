
class Application:
    def __init__(self):
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

    def __make_reservation(self):
        pass

    def __cancel_reservation(self):
        pass

    def __print_schedule(self):
        pass

    def __save_schedule(self):
        pass

    def __exit(self):
        pass