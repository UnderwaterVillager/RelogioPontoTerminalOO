from initial_interfaces import MainMenu
import os


if __name__ == "__main__":
    if not os.path.exists('db/'):
        os.mkdir("db/")
        os.mkdir("db/folhas_diarias/")
    menu = MainMenu()
    menu.run()