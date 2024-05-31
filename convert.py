import os
import codecs
import logging
from googletrans import Translator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

ru_directory = 'C:/practice/finder_translate/org.opencms.locale.ru.jar/org/opencms'

def get_properties_files(directory):
    properties_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.properties'):
                full_path = os.path.join(root, file)
                properties_files.append(full_path)
                logging.info(f'Found properties file: {full_path}')
    return properties_files

def convert_unicode_escape_to_text(file_path):
    with codecs.open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        content = content.encode().decode('unicode_escape')
    with codecs.open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def main():
    ru_files = get_properties_files(ru_directory)
    for file_path in ru_files:
        logging.info(f'Converting Unicode escape to text in file: {file_path}')
        convert_unicode_escape_to_text(file_path)

if __name__ == '__main__':
    main()
