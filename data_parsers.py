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
    } for header in headers}

    row_count = 0
    for row in csv_reader:
        row_count += 1
        for header, value in zip(headers, row):
            if value.strip() == '':
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
        'total_rows': row_count,
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

def summarize_json(data, depth=0, max_depth=3):
    if depth >= max_depth:
        return "..."

    if isinstance(data, dict):
        return summarize_json_object(data, depth, max_depth)
    elif isinstance(data, list):
        return summarize_json_array(data, depth, max_depth)
    else:
        return type(data).__name__

def summarize_json_object(json_obj, depth, max_depth):
    summary = {}
    for key, value in json_obj.items():
        summary[key] = summarize_json(value, depth + 1, max_depth)
    return summary

def summarize_json_array(json_array, depth, max_depth):
    if not json_array:
        return []
    
    sample_item = json_array[0]
    summary = summarize_json(sample_item, depth + 1, max_depth)
    
    return {
        "type": "array",
        "total_items": len(json_array),
        "sample_item": summary
    }

# ... existing code ...
def parse_json(json_content):
    if isinstance(json_content, dict):
        return process_json_object(json_content)
    elif isinstance(json_content, list) and json_content:
        return process_json_array(json_content)
    else:
        return {'type': 'json', 'keys': [], 'data_types': {}}

def process_json_object(json_obj):
    columns_info = {}
    for key, value in json_obj.items():
        data_type = infer_data_type(value)
        columns_info[key] = {
            "data_type": data_type,
            "example_values": [str(value)]  # Truncate long values
        }
    return {
        'type': 'json',
        'total_items': 1,
        'columns': columns_info
    }

def process_json_array(json_array):
    columns_info = {}
    for item in json_array:  # Process up to 10 items
        for key, value in item.items():
            if key not in columns_info:
                columns_info[key] = {
                    "data_type": None,
                    "example_values": []
                }
            data_type = infer_data_type(value)
            if columns_info[key]["data_type"] is None:
                columns_info[key]["data_type"] = data_type
            elif columns_info[key]["data_type"] != data_type:
                columns_info[key]["data_type"] = "mixed"
            if len(columns_info[key]["example_values"]) < 3:
                columns_info[key]["example_values"].append(value)  # Truncate long values

    # Post-processing
    for info in columns_info.values():
        if len(info["example_values"]) > 10:
            info["example_values"] = None
        else:
            info["example_values"] = list(info["example_values"])

    return {
        'type': 'json',
        'total_items': len(json_array),
        'columns': columns_info
    }
