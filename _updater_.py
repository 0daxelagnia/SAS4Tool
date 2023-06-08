import os
import json
import requests
import subprocess
from typing import List

check_list: List[str] = ['items.json', 'main.py', '_utils_.py', '_profile_.py', '_global_.py', '_options_.py', 'start.bat']
repository_url: str = 'https://raw.githubusercontent.com/0daxelagnia/SAS4Tool/main/{}'

def return_file_path(filename: str) -> str:
    return os.path.join(f'{os.getcwd()}', f'{filename}')

def check_updater_is_on() -> bool:
    try:
        with open(return_file_path('config.json'), 'r') as f:
            data: dict = json.load(f)
    except FileNotFoundError:
        with open(return_file_path('config.json'), 'w') as f:
            id = input('Right click to paste your Steam user id: ')
            json.dump({'current_profile': 'Profile0', 'steam_user_id': id, 'updater': True}, f, indent=4)
        return True
    return data['updater']

def check_missing_files() -> List[str]:
    return [return_file_path(i)
            for i in check_list
            if not os.path.exists(return_file_path(i))
            ]

def download_missing_files(files: List[str]) -> None:
    for i in files:
        file_name = os.path.basename(i)
        url = repository_url.format(f'{file_name}')
        r = requests.get(url).text.replace('\r\n', '\n')
        with open(return_file_path(file_name), 'w') as f:
            f.write(r)
        print(f'File {file_name} successfully downloaded.')

def update_old_files(files: List[str]) -> None:
    for i in files:
        dir_file = return_file_path(i)
        file_name = os.path.basename(i)
        url = repository_url.format(f'{file_name}')
        r = requests.get(url).text.replace('\r\n', '\n')
        with open(dir_file, 'r') as f:
            data = f.read()
            if data == r:
                continue
        print(f'Updating {dir_file}...')
        with open(dir_file, 'w') as f:
            f.write(r)

if __name__ == '__main__':
    if not check_updater_is_on():
        subprocess.Popen(['cmd', '/c', 'start.bat'], creationflags=subprocess.CREATE_NEW_CONSOLE)
        exit()
    print('Checking missing files...')
    missing_files = check_missing_files()
    if len(missing_files) > 0:
        print(f'You are missing {len(missing_files)} files\nDownloading missing files...')
        download_missing_files(missing_files)
        print('Done!')
    else:
        print('No files missing.')
    print('Checking for outdated files...')
    update_old_files(check_list)
    print('All files are up to date!\nLaunching main.py...')
    subprocess.Popen(['cmd', '/c', 'start.bat'], creationflags=subprocess.CREATE_NEW_CONSOLE)
    exit()