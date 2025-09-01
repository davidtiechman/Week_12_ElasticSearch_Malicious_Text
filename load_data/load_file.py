import csv
import os
import json
def load_file_txt(file_name):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(BASE_DIR, 'data', file_name)
    arr_weapon = []
    with open(file_path, 'r') as file:
        for name_weapon in file.readlines():
            nwe_name = name_weapon.strip('\n')
            arr_weapon.append(nwe_name)
    return arr_weapon
def load_file_csv(file_name):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(BASE_DIR, 'data', file_name)
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    return data
def write_json(file_name,data):
    with open(file_name, 'w') as file:
        json.dump(data,file_name,indent=2,ensure_ascii=False)

