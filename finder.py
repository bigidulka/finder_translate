import os
import json

de_directory = 'C:/practice/finder_translate/org.opencms.locale.de.jar/org/opencms'
ru_directory = 'C:/practice/finder_translate/org.opencms.locale.ru.jar/org/opencms'

def get_properties_files(directory):
    properties_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.properties'):
                full_path = os.path.join(root, file)
                properties_files.append(full_path)
    return properties_files

def compare_files(de_files, ru_files):
    missing_keys = {}
    for de_file in de_files:
        ru_file = de_file.replace(de_directory, ru_directory).replace('_de', '_ru')
        if ru_file in ru_files:
            with open(de_file, 'r', encoding='ISO-8859-1') as file:
                de_content = file.readlines()
            with open(ru_file, 'r', encoding='ISO-8859-1') as file:
                ru_content = file.readlines()
            de_keys = {line.split('=')[0].strip() for line in de_content if '=' in line}
            ru_keys = {line.split('=')[0].strip() for line in ru_content if '=' in line}
            missing_in_ru = de_keys - ru_keys
            if missing_in_ru:
                missing_keys[ru_file] = list(missing_in_ru)
    return missing_keys

def main():
    de_files = get_properties_files(de_directory)
    ru_files = get_properties_files(ru_directory)

    missing_files = [f.replace(de_directory, ru_directory).replace('_de', '_ru') for f in de_files if f.replace(de_directory, ru_directory).replace('_de', '_ru') not in ru_files]

    missing_keys = compare_files(de_files, ru_files)

    results = {
        'missing_files': missing_files,
        'missing_keys': missing_keys
    }
    with open('results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main()
