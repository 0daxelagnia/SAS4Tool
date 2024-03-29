from _utils_ import option_generator, menu, import_json_to_save, create_json_save, base_path, check_updates
from json import load, dump

def options_menu():
    option_generator(menu["Options"], [
        change_profile,
        manual_edit,
        check_updates
    ])


def change_profile():
    option_generator(menu["Options"]["Change profile"], [
        lambda: set_profile("Profile0"),
        lambda: set_profile("Profile1"),
        lambda: set_profile("Profile2"),
        lambda: set_profile("Profile3"),
        lambda: set_profile("Profile4"),
        lambda: set_profile("Profile5")
    ])


def manual_edit():
    option_generator(menu["Options"]["Manual edit"], [
        create_json_save,
        import_json_to_save
    ])


def set_profile(profile):
    with open(f'{base_path}\\config.json', 'r+') as f:
        data = load(f)
        data['current_profile'] = profile
        f.seek(0)
        dump(data, f, indent=4)
        f.truncate()
    return

