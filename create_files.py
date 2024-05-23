import os
import json

def create_missing_files(json_path):
    """ Creates missing files based on paths listed in a JSON file. """
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        missing_files = data['missing_files']

    for file_path in missing_files:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  
        with open(file_path, 'w', encoding='utf-8') as file:    
            file.write('')  
        print(f'Created: {file_path}')

if __name__ == '__main__':
    json_path = 'results.json'  
    create_missing_files(json_path)
