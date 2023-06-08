import os
import json
import requests


check_list: list = ['items.json', 'main.py', '_utils_.py', '_profile_.py', '_global_.py', '_options_.py', ]
repository_url: str = 'https://raw.githubusercontent.com/0daxelagnia/SAS4Tool/main/{}'


def return_file_path(filename: str) -> str:
    return os.path.join(f'{os.getcwd()}', f'{filename}')


def check_updater_is_on():
    with open(return_file_path('config.json'), 'r') as f:
        data: str = json.load(f)
    return True if data['updater'] else 0


def check_missing_files() -> list:
    return [return_file_path(i)
            for i in check_list
            if not os.path.exists(return_file_path(i))
            ]


def download_missing_files(files: list) -> int:
    for i in files:
        file_name = os.path.basename(i)
        url = repository_url.format(f'{file_name}')
        r: str = requests.get(url).text.replace('\n', '')
        with open(return_file_path(file_name), 'w') as f:
            f.write(r)
        print(f'File {file_name} successfully downloaded.')
    return 0


def update_old_files(files: list):
    
    updated_files = []
    
    for i in files:
        dir_file = return_file_path(i)
        file_name = os.path.basename(i)
        url = repository_url.format(f'{file_name}')
        r = requests.get(url).text
        with open(dir_file, 'r') as f:
            data = f.read()
            if data == r:
                continue
        print(f'Updating {dir_file}...')
        with open(dir_file, 'w') as f:
            f.write(r.replace('\n', ''))
        updated_files.append(file_name)
    print('Done!')

if __name__ == '__main__':
    if not check_updater_is_on():
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
# download_missing_files(check_missing_files())