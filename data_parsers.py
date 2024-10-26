import csv
from helpers import infer_data_type
import re
import json

def parse_csv(file_obj):
    csv_reader = csv.reader(file_obj)
    headers = next(csv_reader, None)
    
    if not headers:
        return {'type': 'csv', 'columns': {}}

    columns_info = {header: {
        "data_type": None,
        "example_values": [],
        "nullable": False,  # Add nullable field
    } for header in headers}

    row_count = 0
    for row in csv_reader:
        row_count += 1
        for header, value in zip(headers, row):
            if value.strip() == '':
                columns_info[header]["nullable"] = True  # Mark as nullable if empty
                continue
            
            data_type = infer_data_type(value)
            if columns_info[header]["data_type"] is None:
                columns_info[header]["data_type"] = data_type
            elif columns_info[header]["data_type"] != data_type:
                columns_info[header]["data_type"] = "mixed"
            
            if len(columns_info[header]["example_values"]) < 3:
                columns_info[header]["example_values"].append(value)

    # Post-processing
    for header, info in columns_info.items():
        if len(info["example_values"]) > 10:
            info["example_values"] = None
        else:
            info["example_values"] = list(info["example_values"])

    return {
        'type': 'csv',
        'columns': columns_info,
    }

def parse_js(file_path):
    if 'data' not in file_path:
        return None
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    json_match = re.search(r'=\s*([\[\{].*[\]\}])\s*$', content, re.DOTALL)
    
    if json_match:
        json_str = json_match.group(1)
        try:
            data = json.loads(json_str)
            return parse_json(data)
        except json.JSONDecodeError:
            print(f"Error decoding JSON in {file_path}")
            return None
    else:
        print(f"No JSON-like structure found in {file_path}")
        return None

def parse_json(json_content):
    return {
        'type': 'json',
        'total_items': 1 if isinstance(json_content, dict) else len(json_content),
        'columns': process_json_content(json_content)
    }

def process_json_content(content):
    if isinstance(content, dict):
        return process_json_object(content)
    elif isinstance(content, list) and content:
        return [process_json_object(item) for item in content[:1]]  # Process up to 3 items
    elif isinstance(content, (str, int, float, bool)):
        return {"data_type": infer_data_type(content) }
    else:
        return {}

def process_json_object(json_obj):
    if not isinstance(json_obj, dict):
        return process_json_content(json_obj)
    
    columns_info = {}
    for key, value in json_obj.items():
        if isinstance(value, (dict, list)):
            # Recursively process nested objects or arrays
            columns_info[key] = process_json_content(value)
        else:
            columns_info[key] = infer_data_type(value)
    return columns_info
