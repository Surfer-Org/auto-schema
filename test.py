import pandas as pd
from ydata_profiling import ProfileReport
import numpy as np
from datetime import datetime

# Create a sample CSV with mixed data types
def create_sample_data():
    data = {
        'text_column': ['hello', 'world', 'test', 'data'],
        'integer_column': [1, 2, 3, 4],
        'float_column': [1.1, 2.2, 3.3, 4.4],
        'date_column': [datetime.now() for _ in range(4)],
        'boolean_column': [True, False, True, False],
        'mixed_column': ['test', '123', '45.6', 'true'],
        'categorical_column': ['A', 'B', 'A', 'B']
    }
    df = pd.DataFrame(data)
    return df

# Function to analyze data types
def analyze_datatypes(df):
    # Generate profile report
    profile = ProfileReport(df, minimal=True, title="Data Type Analysis")
    
    # Get basic data type information
    basic_types = df.dtypes.to_dict()
    
    # Get more detailed information about each column
    detailed_info = {}
    for column in df.columns:
        column_info = {
            'python_type': str(basic_types[column]),
            'unique_values': df[column].nunique(),
            'null_count': df[column].isnull().sum(),
            'sample_values': df[column].head(3).tolist()
        }
        detailed_info[column] = column_info
    
    return basic_types, detailed_info, profile

# Example usage
df = create_sample_data()
basic_types, detailed_info, profile = analyze_datatypes(df)

# Print results
print("Basic Data Types:")
for col, dtype in basic_types.items():
    print(f"{col}: {dtype}")

print("\nDetailed Information:")
for col, info in detailed_info.items():
    print(f"\n{col}:")
    for key, value in info.items():
        print(f"  {key}: {value}")

# Generate HTML report
profile.to_file("data_type_report.html")