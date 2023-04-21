from _utils_ import option_generator, menu, import_save, create_backup, export_save, print_menu, check_int, return_mapped_guns, return_mapped_gun_names, return_gun_category_name, get_input, gun_map, gunStrongbox, gun_map_factions, equipStrongbox, equip_map
import json
from colorama import Fore, init
import random
init()

def profile_menu():
    with open('./config.json') as f:
        data = json.load(f)
        global profile # Set the current profile value to a global variable
        profile = data['current_profile'] 
    
    with open('./items.json', 'r') as f:
        data = json.load(f)
        global gun_dict # Set the guns dictionary to a global variable
        global equip_dict # Set the equipment dictionary to a global variable
        global turret_dict # Set the turret dictionary to a global variable
        gun_dict = dict(data['weapon_info'])
        equip_dict = dict(data['equipment_info'])
        turret_dict = dict(data['turret_info'])

    option_generator(menu["Profile"],
                    [
                        set_items,
                        change_username,
                        set_cash,
                        set_free_skill_reset,
                        set_profile_level,
                        set_black_strongboxes,
                        set_random_stronboxes,
                        set_black_keys,
                        set_aug_cores,
                        support_menu,
                        mp_stats_menu,
                        set_masteries_to_max_level,
                        collections_menu
                    ])

def collections_menu():
    option_generator(menu['Profile']['Unlock all collections'],
                    [
                        lambda: set_all_collections(False),
                        lambda: set_all_collections(True)
                    ])

def set_all_collections(rewards: bool):
    data = import_save()
    create_backup()
    for i in range(len(data['CollectionArrayWeapon'])):
        data['CollectionArrayWeapon'][i]['CollectionUnlocked'] = True
    for i in data['CollectionRewards']:
        data['CollectionRewards'][i] = rewards
    export_save(data=data)
    return 0

def set_masteries_to_max_level():
    max_xp = 542400
    level = 5
    print_menu(menu_dict={}, menu_type=0)
    data = import_save()
    create_backup()
    for i in range(len(data['MasteryProgress'][f'Mastery{profile}'])):
        data['MasteryProgress'][f'Mastery{profile}'][i]['MasteryXp'] = max_xp
        data['MasteryProgress'][f'Mastery{profile}'][i]['MasteryLvl'] = level
    export_save(data=data)
    return 0

def mp_stats_menu():
    option_generator(menu["Profile"]["Set profile multiplayer stats"],
                    [
                        lambda: set_mp_stats('multi_kills'),
                        lambda: set_mp_stats('multi_deaths'),
                        lambda: set_mp_stats('multi_games_won'),
                        lambda: set_mp_stats('multi_games_lost')
                    ])

def set_mp_stats(stat_type: str):
    print_menu(menu_dict={}, menu_type=0)
    amount = check_int(input('Set stat amount\n\n[ > ] '))
    data = import_save()
    create_backup()
    for i in data['Inventory'][profile]['StatsData']:
        if i['key'] == stat_type:
            stat_index = data['Inventory'][profile]['StatsData'].index(i)
    try:
        data['Inventory'][profile]['StatsData'][stat_index]['val'] = amount
    except Exception:
        data['Inventory'][profile]['StatsData'][stat_index]['val'].append({'key': stat_type, 'val': amount})
    export_save(data=data)
    return 0

def support_menu():
    option_generator(menu["Profile"]["Add support items"],
                    [set_turrets,
                    set_grenades])

def grenades_menu():
    option_generator(menu["Profile"]["Add support items"]["Add grenades"],
                    [lambda: set_grenades('grenades_frag'),
                    lambda: set_grenades('grenades_cryo'),])

def set_items():
    option_generator(menu['Profile']['Add items'],
                    [set_guns_menu,
                    set_equipment_menu])

def set_guns_menu():
    option_generator(menu['Profile']['Add items']['Add guns'],
                    [lambda: set_guns_menu_2(0, 0),
                    lambda: set_guns_menu_2(1, 1),
                    lambda: set_guns_menu_2(2, 2),
                    lambda: set_guns_menu_2(1, 3)])

def set_equipment_menu():
    option_generator(menu['Profile']['Add items']['Add equipment'],
                    [lambda: set_equipment_menu_2(0, 0),
                    lambda: set_equipment_menu_2(1, 1),
                    lambda: set_equipment_menu_2(2, 2),
                    lambda: set_equipment_menu_2(1, 3)])

def change_username():
    print_menu(menu_dict={}, menu_type=0)
    name = str(input('Set new username\n\n[ > ] ')) # Input() user for Cash amount
    data = import_save()
    create_backup()
    data['Inventory'][profile]['Name'] = name # Set value to (data['Inventory'][profile]['Money'])
    export_save(data=data)
    return 0

def set_free_skill_reset():
    data=import_save()
    create_backup()
    data['Inventory'][profile]['FreeSkillsReset'] = False
    export_save(data=data)
    return 0

def set_profile_level():
    print_menu(menu_dict={}, menu_type=0)
    xp_array = [0,1071,1288,1655,2176,2855,3696,4704,5883,7237,8770,10486,12390,14486,16778,19270,21966,24871,27989,31324,34880,38661,42672,46917,51400,56125,91145,98978,107193,115797,124795,134195,144002,154222,164863,175930,187430,199368,211752,224587,237880,251637,265865,280569,295756,311433,327605,344279,361461,379158,397375,416120,435398,455215,475579,496495,517970,540009,562620,585808,609580,844923,878201,912282,947176,982890,1019433,1056813,1095038,1134118,1174060,1214873,1256565,1299144,1342620,1387000,1432293,1478507,1525650,1573732,1622760,1672743,1723689,1775606,1828504,1882390,1937273,1993161,2050062,2107986,2166940,3339899,3431459,3524603,3619342,3715690,3813659,3913262,4014512,4117420]
    level = check_int(input('Set new level\n\n[ > ] '))
    total_xp = sum(xp_array[:level])
    data = import_save()
    create_backup()
    data['Inventory'][profile]['Skills']['PlayerLevel'] = level
    data['Inventory'][profile]['Skills']['PlayerTotalXp'] = total_xp
    export_save(data=data)
    return 0

def set_black_strongboxes():
    print_menu(menu_dict={}, menu_type=0)
    amount = check_int(input('Set amount of black strongboxes\n\n[ > ] '))
    strongboxes_amount = [random.randint(10000000, 999999999) for _ in range(amount)]
    data = import_save()
    create_backup()
    data['Inventory'][profile]['Skills']['AvailableBlackStrongboxes'] = strongboxes_amount
    export_save(data=data)
    return 0

def set_random_stronboxes():
    return 0

def set_black_keys():
    print_menu(menu_dict={}, menu_type=0)
    amount = check_int(input('Set amount of black keys\n\n[ > ] '))
    data = import_save()
    create_backup()
    data['Inventory'][profile]['Skills']['AvailableBlackKeys'] = amount
    export_save(data=data)
    return 0

def set_aug_cores():
    print_menu(menu_dict={}, menu_type=0)
    amount = check_int(input('Set amount of augment cores\n\n[ > ] '))
    data = import_save()
    create_backup()
    data['Inventory'][profile]['Skills']['AvailableEliteAugmentCores'] = amount
    export_save(data=data)
    return 0

def set_grenades(grenade_type: str):
    data = import_save()
    amount = check_int(input(f'Set amount of grenades\n\n[ > ] '))
    create_backup()
    data['Inventory'][profile]['Ammo'][grenade_type] = amount
    export_save(data=data)
    return 0

def set_turrets():
    options = []
    options_parent = []
    
    data = import_save()
    amount = check_int(input('Set amount of turrets\n\n[ > ] '))
    create_backup()
    profile_level = int(data['Inventory'][profile]['Skills']['PlayerLevel'])
    turret_type = 'red' if profile_level >= 30 else 'normal'
    for i in range(len(turret_dict[turret_type])):
        options.append(f'[{i+1}] {turret_dict[turret_type][i]["Name"]}')
        options_parent.append(f'{i+1}')
    options.append(f"\n[ESC] Back")
    for i in range(len(options_parent)):
        if type(options_parent[i]) == str:
            options_parent[i] = options_parent[i].upper()
    print_menu(menu_type=0)
    for i in range(len(options)):
        print(options[i])
    choice = get_input()
    if choice == 'ESC':
        return 0
    if choice in options_parent:
        choice_index = options_parent.index(choice)
        turret_id = turret_dict[turret_type][choice_index]['ID']
        try:
            for i in data['Inventory'][profile]['Turrets']:
                if i['TurretId'] == turret_id:
                    i['TurretCount'] = amount
        except Exception:
            data['Inventory'][profile]['Turrets'].append({'TurretId': turret_id, 'TurretCount': amount})
        export_save(data=data)
    else:
        return

def set_equipment_menu_2(equip_version: int, index: int):
    options = []
    options_parent = []
    path = equip_dict
    
    equip_version_name = list(path.keys())[index]
    equip_types = list(path[equip_version_name])
    
    for i in range(len(equip_types)):
        equip_types[i] = equip_types[i].capitalize()
        if '_' in equip_types[i]:
                equip_types[i] = equip_types[i].replace('_', ' ')
        if i >= 9:
            options.append(f'[{chr(65 + i - 9)}] {equip_types[i]}')
            options_parent.append(f'{chr(65 + i - 9)}')
        else:
            options.append(f'[{i+1}] {equip_types[i]}')
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
        equipment = path[equip_version_name][equip_types[choice_index].lower().replace(' ', '_')]
        set_equipment(equip_version, choice_index, equipment)
    else:
        return

def set_equipment(equip_version, choice_index, equipment_list):
    
    equip_type = equip_map[choice_index]
    
    options = []
    options_parent = []
    
    for i in range(len(equipment_list)):
        if i >= 9:
            options.append(f'[{chr(65 + i - 9)}] {equipment_list[i]["Name"]}')
            options_parent.append(f'{chr(65 + i - 9)}')
        else:
            options.append(f'[{i+1}] {equipment_list[i]["Name"]}')
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
        equip_id = equipment_list[choice_index]['ID']
        print_menu(menu_type=0)
        print(f'{Fore.RED}[WARNING]{Fore.RESET} Using letters or going higher/lower will crash your game.')
        bonus = int(input('Set item bonus stats [0-10]: '))
        augments = int(input('Set item augments [0-3]: '))
        grade = int(input('Set item grade [0-12]: '))
        strongbox = dict(equipStrongbox)
        strongbox['ID'] = equip_id
        strongbox['EquipVersion'] = equip_version
        strongbox['BonusStatsLevel'] = bonus
        strongbox['Grade'] = grade
        strongbox['AugmentSlots'] = augments
        strongbox['InventoryIndex'] = equip_type
        strongbox['EquippedSlot'] = equip_type
        data = import_save()
        create_backup()
        data['Inventory'][profile]['Strongboxes']['Claimed'].append(1)
        data['Inventory'][profile]['Strongboxes']['Claimed'].append(strongbox)
        data['Inventory'][profile]['Strongboxes']['Claimed'].append(8)
        data['Inventory'][profile]['Strongboxes']['Claimed'].append(0)
        export_save(data=data)
        return 0
    else:
        return

def set_guns_menu_2(gun_version: int, index: int):
    options = []
    options_parent = []
    path = gun_dict
    
    gun_version_name = list(path.keys())[index]
    gun_types = list(path[gun_version_name])
    
    for i in range(len(gun_types)):
        gun_types[i] = gun_types[i].capitalize()
        if '_' in gun_types[i]:
                gun_types[i] = gun_types[i].replace('_', ' ')
        if i >= 9:
            options.append(f'[{chr(65 + i - 9)}] {gun_types[i]}')
            options_parent.append(f'{chr(65 + i - 9)}')
        else:
            options.append(f'[{i+1}] {gun_types[i]}')
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
        guns = path[gun_version_name][gun_types[choice_index].lower().replace(' ', '_')]
        set_gun(gun_version, choice_index, guns, index)
    else:
        return

def set_gun(gun_version: int, choice_index: int, guns_list: list, gun_version_index: int):
    if gun_version_index == 3:
        gun_type = gun_map_factions[choice_index]
    else:
        gun_type = gun_map[choice_index]
    
    options = []
    options_parent = []
    for i in range(len(guns_list)):
        if i >= 9:
            options.append(f'[{chr(65 + i - 9)}] {guns_list[i]["Name"]}')
            options_parent.append(f'{chr(65 + i - 9)}')
        else:
            options.append(f'[{i+1}] {guns_list[i]["Name"]}')
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
        gun_id = guns_list[choice_index]['ID']
        
        print_menu(menu_type=0)
        print(f'{Fore.RED}[WARNING]{Fore.RESET} Using letters or going higher/lower will crash your game.')
        bonus = int(input('Set item bonus stats [0-10]: '))
        augments = int(input('Set item augments [0-4]: '))
        grade = int(input('Set item grade [0-12]: '))
        strongbox = dict(gunStrongbox)
        strongbox['ID'] = gun_id
        strongbox['EquipVersion'] = gun_version
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
        export_save(data=data)
        return 0
    else:
        return

def set_cash():
    print_menu(menu_dict={}, menu_type=0)
    money = check_int(int(input('Set SAS cash amount\n\n[ > ] '))) # Input() user for Cash amount
    data = import_save()
    create_backup()
    data['Inventory'][profile]['Money'] = money # Set value to (data['Inventory'][profile]['Money'])
    export_save(data=data)
    return 0