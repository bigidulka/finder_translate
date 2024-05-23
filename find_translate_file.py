import os
import codecs
import json
import logging
from googletrans import Translator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

de_directory = 'C:/practice/finder_translate/org.opencms.locale.de.jar/org/opencms'
ru_directory = 'C:/practice/finder_translate/org.opencms.locale.ru.jar/org/opencms'

def get_properties_files(directory):
    """ Walk through the directory and collect all .properties files. """
    properties_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.properties'):
                full_path = os.path.join(root, file)
                properties_files.append(full_path)
                logging.info(f'Found properties file: {full_path}')
    return properties_files

def translate_and_create_files(de_files, ru_directory):
    """ Translate and create missing files if needed. """
    translator = Translator()
    results = {'created_files': [], 'translated_entries': {}}

    for de_file in de_files:
        ru_file = de_file.replace(de_directory, ru_directory).replace('_de', '_ru')
        # Check if the Russian file exists
        if not os.path.exists(ru_file):
            os.makedirs(os.path.dirname(ru_file), exist_ok=True)
            results['created_files'].append(ru_file)
            logging.info(f'Created missing Russian file: {ru_file}')

        # Translate content
        with open(de_file, 'r', encoding='ISO-8859-1') as file:
            de_content = file.readlines()

        de_dict = {line.split('=')[0].strip(): line.split('=')[1].strip() for line in de_content if '=' in line}

        with codecs.open(ru_file, 'w', encoding='utf-8') as file:
            for key, value in de_dict.items():
                try:
                    translated = translator.translate(value, dest='ru', src='de').text
                    file.write(f'{key}={translated}\n')
                    results['translated_entries'].setdefault(ru_file, []).append(key)
                    logging.info(f'Translated and added "{key}" to {ru_file}')
                except Exception as e:
                    logging.error(f'Failed to translate key {key}: {e}')

    return results

def main():
    de_files = get_properties_files(de_directory)
    results = translate_and_create_files(de_files, ru_directory)

    with open('translation_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main()
