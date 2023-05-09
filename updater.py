import requests
import json
import os
import filecmp


latest = '3.0.3'

needed_files = [os.path.join('.', 'items.json')]
source_code_files = [os.path.join('.', 'main.py'), os.path.join('.', '_utils.py_'), os.path.join('.', '_profile_.py'), os.path.join('.', '_options_.py'), os.path.join('.', '_global_.py')]

gh_items: str = 'https://raw.githubusercontent.com/0daxelagnia/SAS4Tool/main/items.json'
releases_url: str = f'https://github.com/0daxelagnia/SAS4Tool/releases/download/{latest}/'

def check_py_updater_ver():
    updater_content = requests.get('https://raw.githubusercontent.com/0daxelagnia/SAS4Tool/main/updater.py')
    open('updater.tmp', 'wb').write(updater_content.text.encode('utf-8'))
    file_self = os.path.join('.', 'updater.py')
    temp_file = os.path.join('.', 'updater.tmp')
    
    py_file_size = file_self.__sizeof__()
    tmp_file_size = temp_file.__sizeof__() - 1
    
    if py_file_size == tmp_file_size:
        print('file is the same!')


def check_compiled_updater_ver():
    ...


check_py_updater_ver()
