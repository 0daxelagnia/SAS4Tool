import msvcrt
from colorama import Fore, init
import time
from kucingoren.gameio import get_game_save_path
from kucingoren.gameio import dgdata
import json
from os import mkdir as _mkdir, chdir as _chdir, path as _path, remove as _remove, getcwd, name as _name, system as _sys, startfile
from io import BytesIO
from datetime import datetime
from shutil import copyfile
import tkinter as tk
from tkinter import filedialog

init()

def loadProfile() -> tuple:
    if not _path.exists('.\config.json'):
        with open('config.json', 'w') as f:
            data: dict = {
        'current_profile': 'Profile0',
        'steam_user_id': None
    }
            json.dump(data, f, indent=4)
    with open('.\config.json', 'r') as f:
        data: dict = json.load(f)
        if data['steam_user_id'] is not None:
            STEAM_USER_ID: str = data['steam_user_id']
        else:
            print(f'{Fore.RED}[ERROR] {Fore.LIGHTWHITE_EX}| The steam user ID must be specified in config.json.')
            exit()
    return data['current_profile'], STEAM_USER_ID

save_path: str = get_game_save_path( loadProfile()[1] )
save_data: dict = {}
base_path: str = getcwd()
version: str = '3.0.0'
dev: str = '<\\>#0077'

def clear_screen():
    _sys('cls' if _name == 'nt' else 'clear')

def get_input() -> (int | str):
    time.sleep(0.25)
    key = msvcrt.getch()
    if key == b'\x1b': # ESC key
        return 'esc'
    elif key.isdigit():
        return str(key, 'utf-8')
    else:
        try:
            return str(key.upper(), 'utf-8')
        except UnicodeDecodeError:
            return 'invalid key'

def generate_menu_options(menu_dict):
    options = []
    for index, (key, value) in enumerate(menu_dict.items()): 
        if index >= 9: # If index is greater than or equal to 9, use letters for options
            letter = chr(65 + index - 9) # Determine letter option using chr() and ASCII codes for capital letters
            options.append(f"[{letter}] {(key.capitalize()).replace('_', ' ')}")
        else: # Use numbers for options
            options.append(f"[{index+1}] {(key.capitalize()).replace('_', ' ')}")
    options.append(f"\n[ESC] Back")
    return "\n".join(options) # Join the list of options into a single string with newline separators

def generate_menu_for_lists(option_list: list):
    # do the same as generate_menu_option but instead of taking an input of a dictionary, take a list instead
    for i in range(len(option_list)):
        option_list[i] = f"[{i+1}] {option_list[i]}"
        if i >= 9:
            option_list[i] = f"[{chr(65 + i - 9)}] {option_list[i]}"
        if '_' in option_list[i]:
            option_list[i] = option_list[i].replace('_', ' ')
    option_list.append(f"\n[ESC] Back")
    return "\n".join(option_list)

def print_menu(menu_dict: dict = None, menu_type: int = None, option_list: list = None) -> None:
    main_title = f'''{Fore.RED}
                   _______   ______________          __
                  / __/ _ | / __/ / /_  __/__  ___  / /
                 _\ \/ __ |_\ \/_  _// / / _ \/ _ \/ / 
                /___/_/ |_/___/ /_/ /_/  \___/\___/_/  

                 { Fore.LIGHTRED_EX }version: { version } | made by: { dev }

{Fore.LIGHTWHITE_EX}Current profile: {Fore.LIGHTGREEN_EX}{loadProfile()[0].replace('e', 'e ')}
{Fore.LIGHTWHITE_EX}'''
    clear_screen()
    
    if menu_type != 0:
        print(main_title)
        options = generate_menu_options(menu_dict)
        print(options + "\n\n[ > ] ", end='', flush=True)
    else:
        print(main_title)

def handle_menu_option(choice, functions):
    if choice == 'esc':
        return 0
    
    if choice == 'invalid key':
        print('Invalid option!')
        time.sleep(1)
        return
    elif choice.isdigit():
        try:
            function = functions[int(choice)-1]
        except Exception:
            print('Invalid option!')
            time.sleep(1)
            return
        return function()
    else:
        try:
            function = functions[ord(choice.lower()) - 97 + 9]
        except Exception:
            print('Invalid option!')
            time.sleep(1)
            return
        return function()

def option_generator(menu_path: dict, functions: list):
    while True:
        print_menu(menu_path, 1)
        choice = get_input()
        if choice == 'esc':
            return
        return_value = handle_menu_option(choice, functions)
        if return_value == 0:
            return

def option_generator_for_lists(option_list: list, functions: list):
    while True:
        print_menu(option_list, 0)
        choice = get_input()
        if choice == 'esc':
            return
        return_value = handle_menu_option(choice, functions)
        if return_value == 0:
            return

def import_save () -> str:
    save_bytes = b"".join( dgdata.iter_decode(save_path.open("rb")) )
    return json.loads( save_bytes )

def export_save ( data: str ) -> None:
    save_bytes = json.dumps( data ).encode( "utf8" )
    dgdata.write_encode( save_path.open("wb+"), BytesIO(save_bytes) )

def create_backup () -> None:
    backup_time = datetime.now().strftime( "%Y-%m-%d.%H-%M-%S" )
    if not _path.exists('Backups'):
        _mkdir('Backups')
    _chdir('Backups')
    backup_path = (f"{save_path.stem}-{backup_time}{save_path.suffix}")
    copyfile(save_path, backup_path)
    _chdir(base_path)
    return 0

def create_json_save() -> None:
    if not _path.exists('Exports'):
        _mkdir('Exports')
    _chdir('Exports')
    save = import_save()
    with open('save_exported.json', 'w') as f:
        json.dump(save, f, indent=4)
    _chdir(base_path)
    return 0

def import_json_to_save() -> None:
    root = tk.Tk()
    root.withdraw()
    root.wm_attributes("-topmost", 1) # Make the window appear on top
    root.title("Select your exported save file")
    data_path = filedialog.askopenfilename(initialdir=base_path, filetypes=[("JSON file(s)", "*.json")])
    root.destroy()
    with open(data_path, 'r') as f:
        data = json.load(f)
    export_save(data=data)
    return 0

def check_int(value) -> int:
    if type(value) == int and value >= 0:
        return value
    print("\n\nInvalid amount!")
    time.sleep(1)
    return 0

def return_mapped_guns(index: int) -> int:
    return gun_map.get(index)

def return_mapped_gun_names(index: int) -> str:
    return gun_map_names.get(index)

def return_gun_category_name(index: int) -> str:
    cat_map = {
        0: "normal",
        1: "red",
        2: "black",
        3: "factions"
    }
    return cat_map.get(index)

gun_map = {
    0: 1,#'pistols'
    1: 2, #'smg'
    2: 3, #'assault_rifle'
    3: 4, #'shotgun'
    4: 5, #'sniper'
    5: 6, #'rocket_launcher'
    6: 8, #'flame_thrower'
    7: 9, #'lmg'
    8: 10, #'disk_thrower'
    9: 11, #'laser'
}

equip_map = {
    0: 1, # 'helmet'
    1: 2, # 'vest'
    2: 3, # 'gloves'
    3: 5, # 'pants'
    4: 4, # 'boots'
}

gun_map_factions = {
    0: 1,
    1: 3,
    2: 4,
    3: 6,
    4: 8,
    5: 9,
    6: 10,
    7: 11
}

gun_map_names = {
    0: 'pistols',
    1: 'smg',
    2: 'assault_rifle',
    3: 'shotgun',
    4: 'sniper',
    5: 'rocket_launcher',
    6: 'flame_thrower',
    7: 'lmg',
    8: 'disk_thrower',
    9: 'laser',
}

menu = {
    "Global": {
        "Factions": {
            "Set faction guild": {
                    "GUARDIANS": {},
                    "NOMADS": {},
                    "OUTLAWS": {},
                    "VANGUARD": {},
                    "SPARTANS": {}
                },
            "Set faction credits": {
                "Zeta credits": {},
                "Epsilon credits": {},
                "Sigma credits": {},
                "Xi credits": {},
                "Omicron credits": {},
                "Faction credits": {},
                "All credits": {}
            }
        },
        "Premium Items": {},
        "Revive Tokens": {},
        "Premium nightmare tickets": {},
        "Remove ads": {},
        "Unlock Profile (5 & 6)": {},
        "Unlock fairground pack": {}
    },
    "Profile": {
        "Add items": {
                "Add guns": {
                        "Normal": {},
                        "Red": {},
                        "Black": {},
                        "Factions": {}
                    },
                "Add equipment": {
                        "Normal": {},
                        "Red": {},
                        "Black": {},
                        "Factions": {}
                    }
            },
        "Change username": {},
        "Add SAS cash": {},
        "Set free skill reset": {},
        "Set profile level": {},
        "Add black strongboxes": {},
        "Add random strongboxes [Work in progress |  Blank]": {},
        "Add black keys": {},
        "Add augment cores": {},
        "Add support items": {
                "Add turrets": {},
                "Add grenades": {
                    "Frag grenade": {},
                    "Cryo grenade": {}
                }
            },
        "Set profile multiplayer stats": {
                "MP Kills": {},
                "MP Deaths": {},
                "MP Games won": {},
                "MP Games lost": {}
            },
        "Set profile masteries to max level": {},
        "Unlock all collections": {
                "With strongboxes": {},
                "Without strongboxes": {}
        }
        },
    "Options": {
        "Change profile": {
            "Profile 1": {},
            "Profile 2": {},
            "Profile 3": {},
            "Profile 4": {},
            "Profile 5": {},
            "Profile 6": {}
        },
        "Manual edit": {
            "Export to JSON": {},
            "Import JSON to .save": {}
        }
    }
}

gunStrongbox = {
    "ID": 0,
    "EquipVersion": 0,
    "Grade": 0,
    "EquippedSlot": -1,
    "AugmentSlots": 0,
    "InventoryIndex": 0,
    "Seen": False,
    "BonusStatsLevel": 0,
    "Equipped": False,
    "ContainsKey": False,
    "ContainsAugmentCore": False,
    "BlackStrongboxSeed": 0,
    "UseDefaultOpenLogic": True
}

equipStrongbox = {
    "ID": 0,
    "EquipVersion": 0,
    "Grade": 0,
    "EquippedSlot": 0,
    "AugmentSlots": 0,
    "InventoryIndex": -1,
    "Seen": False,
    "BonusStatsLevel": 0,
    "Equipped": False,
    "ContainsKey": False,
    "ContainsAugmentCore": False,
    "BlackStrongboxSeed": 0,
    "UseDefaultOpenLogic": True
}