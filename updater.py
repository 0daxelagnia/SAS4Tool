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
    if filecmp.cmp('updater.py', 'updater.tmp'):
        print('file is the same')
    else:
        print('file is not the same')


def check_compiled_updater_ver():
    ...


check_py_updater_ver()
