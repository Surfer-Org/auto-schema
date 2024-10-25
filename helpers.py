def infer_data_type(value):
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
