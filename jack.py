import os
import json
import pandas as pd
import numpy as np
from json import JSONEncoder

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(CustomJSONEncoder, self).default(obj)

def analyze_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        
        columns_info = {}
        for column in df.columns:
            column_info = {
                "dtype": str(df[column].dtype),
                "unique_values": int(df[column].nunique()),
                "null_count": int(df[column].isnull().sum()),
                "sample_values": df[column].head(3).tolist(),
                "options": df[column].unique().tolist() if df[column].nunique() <= 10 else None
            }
            columns_info[column] = column_info
        
        return columns_info
    except Exception as e:
        return {"error": str(e)}

def document_structure(root_dir):
    def process_directory(dir_path):
        structure = {"files": [], "folders": []}

        for item in os.listdir(dir_path):
            item_path = os.path.join(dir_path, item)
            
            if os.path.isfile(item_path):
                if item == '.DS_Store':
                    continue
                structure["files"].append(process_file(item, item_path))
            elif os.path.isdir(item_path):
                structure["folders"].append({
                    "name": item,
                    "contents": process_directory(item_path)
                })

        return structure

    def process_file(filename, file_path):
        file_ext = os.path.splitext(filename)[1].lower()
        file_info = {
            "name": filename,
            "type": file_ext
        }
        if file_ext == '.csv':
            file_info["columns"] = analyze_csv(file_path)
        return file_info

    return process_directory(root_dir)

def main():
    root_dir = r"C:\Users\sahil\Downloads\Complete_LinkedInDataExport_10-22-2024"
    structure = document_structure(root_dir)
    with open('output_structure.json', 'w', encoding='utf-8') as json_file:
        json.dump(structure, json_file, indent=4)

if __name__ == "__main__":
    main()