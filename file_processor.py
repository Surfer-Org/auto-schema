import os
import zipfile
import tarfile
import io
from data_parsers import *
import json

def process_file(file_path, file_obj=None):
    if file_path.endswith('.csv'):
        if file_obj:
            text_file = io.TextIOWrapper(file_obj, encoding='utf-8')
            return parse_csv(text_file)
        with open(file_path, 'r', encoding='utf-8') as csv_file:
            return parse_csv(csv_file)
    elif file_path.endswith('.json'):
        if file_obj:
            text_file = io.TextIOWrapper(file_obj, encoding='utf-8')
            json_content = json.load(text_file)
        else:
            with open(file_path, 'r', encoding='utf-8') as json_file:
                json_content = json.load(json_file)
        return parse_json(json_content)

    elif file_path.endswith('.js'): # THIS IS MEANT FOR TWITTER ARCHIVE!!
        return parse_js(file_path)
    else:
        return None

def get_files_structure(folder_path, current_level=None):
    if current_level is None:
        current_level = {}

    if os.path.isdir(folder_path):
        for root, dirs, files in os.walk(folder_path):
            relative_path = os.path.relpath(root, folder_path)
            sub_level = current_level
            if relative_path != '.':
                for part in relative_path.split(os.sep):
                    sub_level = sub_level.setdefault(part, {})
            for file in files:
                if file != '.DS_Store':  # Skip .DS_Store files
                    file_path = os.path.join(root, file)
                    result = process_file(file_path)
                    if result is not None:
                        sub_level[file] = result

    elif zipfile.is_zipfile(folder_path):
        with zipfile.ZipFile(folder_path, 'r') as zip_ref:
            for file in zip_ref.namelist():
                if not file.endswith('.DS_Store'):  # Skip .DS_Store files
                    parts = file.split('/')
                    sub_level = current_level
                    for part in parts[:-1]:
                        sub_level = sub_level.setdefault(part, {})
                    if parts[-1]:
                        with zip_ref.open(file) as file_obj:
                            result = process_file(file, file_obj)
                            if result is not None:
                                sub_level[parts[-1]] = result

    elif tarfile.is_tarfile(folder_path):
        with tarfile.open(folder_path, 'r:gz') as tar_ref:
            for member in tar_ref.getmembers():
                if member.isfile() and not member.name.endswith('.DS_Store'):  # Skip .DS_Store files
                    file = member.name
                    parts = file.split('/')
                    sub_level = current_level
                    for part in parts[:-1]:
                        sub_level = sub_level.setdefault(part, {})
                    extracted_path = tar_ref.extractfile(member)
                    result = process_file(file, extracted_path)
                    if result is not None:
                        sub_level[parts[-1]] = result

    elif os.path.isfile(folder_path):
        if not folder_path.endswith('.DS_Store'):  # Skip .DS_Store files
            return process_file(folder_path)
    else:
        current_level['error'] = 'Unsupported file or folder type. You can add support for this type if needed.'

    return current_level
