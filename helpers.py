from dateutil.parser import parse
from dateutil.parser import ParserError
import re

def infer_data_type(value):
    if isinstance(value, str):
        # Check if the string is a number first
        if re.match(r'^-?\d+(\.\d+)?$', value):
            return 'float' if '.' in value else 'integer'
        
        # Try to parse as date
        try:
            # Add a check for reasonable year range
            date = parse(value, fuzzy=False)
            if 1000 <= date.year <= 9999:
                return 'date'
        except (ParserError, OverflowError, ValueError):
            pass
    
    data_type = type(value).__name__
    
    type_mapping = {
        'bool': 'boolean',
        'int': 'integer',
        'float': 'float',
        'str': 'string',
        'list': 'array',
        'dict': 'object',
        'NoneType': 'null'
    }
    
    return type_mapping.get(data_type, data_type)
