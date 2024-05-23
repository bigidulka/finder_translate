import os
import codecs
import logging
from googletrans import Translator, LANGUAGES

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

de_directory = 'C:/practice/finder_translate/org.opencms.locale.de.jar/org/opencms'
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

def compare_and_translate_files(de_files, ru_files, from_lang='de', to_lang='ru'):
    translator = Translator()
    for de_file in de_files:
        ru_file = de_file.replace(de_directory, ru_directory).replace('_de', '_ru')
        if ru_file in ru_files:
            logging.info(f'Comparing files {de_file} and {ru_file}')
            with open(de_file, 'r', encoding='ISO-8859-1') as file:
                de_content = file.readlines()
            with open(ru_file, 'r', encoding='ISO-8859-1') as file:
                ru_content = file.readlines()
            de_dict = {line.split('=')[0].strip(): line.split('=')[1].strip() for line in de_content if '=' in line}
            ru_keys = {line.split('=')[0].strip() for line in ru_content if '=' in line}
            missing_keys = set(de_dict.keys()) - ru_keys

            if missing_keys:
                logging.info(f'Missing keys in {ru_file}: {missing_keys}')
                with codecs.open(ru_file, 'a', encoding='utf-8') as file:
                    for key in missing_keys:
                        value = de_dict[key]
                        try:
                            translated = translator.translate(value, dest=to_lang, src=from_lang)
                            utf8_encoded = translated.text.encode('unicode_escape')
                            file.write(f'{key}={utf8_encoded.decode("utf-8")}\n')
                            logging.info(f'Translated and added "{key}" to {ru_file}')
                        except Exception as e:
                            logging.error(f'Failed to translate key {key}: {e}')
        else:
            logging.warning(f'No corresponding Russian file found for {de_file}')

def main():
    de_files = get_properties_files(de_directory)
    ru_files = get_properties_files(ru_directory)
    compare_and_translate_files(de_files, ru_files)

if __name__ == '__main__':
    main()
