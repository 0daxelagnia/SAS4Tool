from _utils_ import option_generator, menu, import_save, create_backup, export_save, print_menu, check_int, get_input,gunStrongbox
import time, json
from colorama import Fore, init
init()

def global_menu():
    option_generator(menu['Global'],
                    [factions_menu,
                    add_premium_guns,
                    set_revive,
                    set_nightmare,
                    remove_ads,
                    unlock_profiles,
                    unlock_fairground_pack])

def add_premium_guns():
    options = []
    options_parent = []
    fixed_names = []
    with open('./items.json', 'r') as f:
        data = json.load(f)
        prem_dict = data['premium_info']
    
    with open('./config.json', 'r') as f:
        data = json.load(f)
        profile = data['current_profile'] 

    for i in prem_dict:
        fixed_names.append(f"sas4_{i['Name'].lower().replace('.', '').replace(' ', '')}")
    for i in range(len(prem_dict)):
        if i >= 9:
            options.append(f'[{chr(65 + i - 9)}] {prem_dict[i]["Name"]}')
            options_parent.append(f'{chr(65 + i - 9)}')
        else:
            options.append(f'[{i+1}] {prem_dict[i]["Name"]}')
            options_parent.append(f'{i+1}')
        '\n'.join(options)
    for i in range(len(options_parent)):
        if type(options_parent[i]) == str:
            options_parent[i] = options_parent[i].upper()
    options.append(f"\n[ESC] Back")
    print_menu(menu_type=0)
    for i in range(len(options)):
        print(options[i])
    choice = get_input()
    if choice == 'ESC':
        return 0
    if choice in options_parent:
        choice_index = options_parent.index(choice)
        gun_id = prem_dict[choice_index]['ID']
        gun_type = prem_dict[choice_index]['Type']
        gun_name = fixed_names[choice_index]
        
        print_menu(menu_type=0)
        print(f'{Fore.RED}[WARNING]{Fore.RESET} Using letters or going higher/lower will crash your game.')
        bonus = int(input('Set item bonus stats [0-10]: '))
        augments = int(input('Set item augments [0-4]: '))
        grade = int(input('Set item grade [0-12]: '))
        strongbox = dict(gunStrongbox)
        strongbox['ID'] = gun_id
        strongbox['EquipVersion'] = 1
        strongbox['BonusStatsLevel'] = bonus
        strongbox['Grade'] = grade
        strongbox['AugmentSlots'] = augments
        strongbox['InventoryIndex'] = gun_type
        
        data = import_save()
        create_backup()
        data['Inventory'][profile]['Strongboxes']['Claimed'].append(0)
        data['Inventory'][profile]['Strongboxes']['Claimed'].append(strongbox)
        data['Inventory'][profile]['Strongboxes']['Claimed'].append(8)
        data['Inventory'][profile]['Strongboxes']['Claimed'].append(0)
        
        for i in range(len(data['PurchasedIAP']['PurchasedIAPArray'])):
            if data['PurchasedIAP']['PurchasedIAPArray'][i]['Identifier'] == gun_name:
                data['PurchasedIAP']['PurchasedIAPArray'][i]['Value'] = True
        export_save(data=data)
        return 0

def unlock_fairground_pack():
    data = import_save()
    create_backup()
    data['PurchasedIAP']['PurchasedIAPArray'][15]['Value'] = True
    data['PurchasedIAP']['PurchasedIAPArray'][16]['Value'] = True
    export_save(data=data)
    return 0

def factions_menu():
    option_generator(menu['Global']['Factions'],
                    [set_faction_guild,
                    set_faction_credits])

def set_faction_guild():
    option_generator(menu["Global"]["Factions"]["Set faction guild"],
                    [lambda: set_guild("GUARDIANS"),
                    lambda: set_guild("NOMADS"),
                    lambda: set_guild("OUTLAWS"),
                    lambda: set_guild("VANGUARD"),
                    lambda: set_guild("SPARTANS")])

def set_faction_credits():
    option_generator(menu["Global"]["Factions"]["Set faction credits"],
                    [lambda: set_credits('Zeta credits', 0),
                    lambda: set_credits('Epsilon credits', 1),
                    lambda: set_credits('Sigma credits', 2),
                    lambda: set_credits('Xi credits', 3),
                    lambda: set_credits('Omicron credits', 4),
                    lambda: set_credits('Faction credits', 0),
                    lambda: set_credits('All credits', 0)])

def unlock_profiles():
    data = import_save()
    create_backup()
    for i in range(2):
        data['Global']['PurchasedIAP']['PurchasedIAPArray'][i]['Identifier'] = True
    export_save(data=data)
    return 0

def remove_ads():
    data = import_save()
    create_backup()
    data['Global']['ForceRemoveAds'] = True
    export_save(data=data)
    return 0

def set_nightmare():
    print_menu(menu_dict={}, menu_type=0)
    nightmare_tokens = check_int(int(input('Set nightmare tokens amount\n\n[ > ] ')))
    data = import_save()
    create_backup()
    data['Global']['AvailablePremiumTickets'] = nightmare_tokens
    export_save(data=data)
    return 0

def set_revive():
    print_menu(menu_dict={}, menu_type=0)
    revive = check_int(int(input('Set revive tokens amount\n\n[ > ] ')))
    data = import_save()
    create_backup()
    data['Global']['ReviveTokens'] = revive
    export_save(data=data)
    return 0

def set_credits(credit_type: str, planet_index: int):
    print_menu(menu_dict={},menu_type=0)
    credits = check_int(int(input(f'Set your {credit_type}\n\n[ > ] ')))
    data = import_save()
    create_backup()
    if credit_type == 'All credits':
        data['FactionWarCredits'] = credits
        for planet in data['FactionWarPlanetArray']:
            planet['Currency'] = credits
    elif credit_type == 'Faction credits':
        data['FactionWarCredits'] = credits
    else:
        create_backup()
        data['FactionWarPlanetArray'][planet_index]['Currency'] = credits
    export_save(data=data)
    return 0

def set_guild(guild: str):
    data = import_save()
    create_backup()
    data['CurrentFactionWarFaction'] = guild
    export_save(data=data)
    return 0