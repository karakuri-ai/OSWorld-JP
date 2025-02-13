import os
import json

def update_json_id(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    if 'id' in data and not data['id'].startswith('J_'):
        data['id'] = 'J_' + data['id']
    
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                update_json_id(file_path)

process_directory('examples_japanese')