import os
import re

def find_file_with_text(directory, search_text):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                    if re.search(search_text, content):
                        print(f"Файл '{filename}' содержит текст '{search_text}'")
                        print(f"Полный путь к файлу: {os.path.abspath(filepath)}")
            except (UnicodeDecodeError, FileNotFoundError):
                pass

directory_to_search = 'org.opencms.locale.ru.jar'
text_to_search = "gui_editor"
find_file_with_text(directory_to_search, text_to_search)
