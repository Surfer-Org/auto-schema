import json
from datetime import datetime
from file_processor import get_files_structure

def export_to_json(folder_path):
    files_structure = get_files_structure(folder_path)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"sahil_schema.json"
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(files_structure, json_file, indent=4)

def main():
    folder_path = r"C:\Users\sahil\Downloads\Complete_LinkedInDataExport_10-22-2024.zip"
    export_to_json(folder_path)

if __name__ == "__main__":
    main()