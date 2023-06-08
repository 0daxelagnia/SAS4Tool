from _utils_ import menu, option_generator
from _global_ import global_menu
from _profile_ import profile_menu
from _options_ import options_menu


def main_menu():
    option_generator(menu, [global_menu, profile_menu, options_menu])


if __name__ == "__main__":
    main_menu()
