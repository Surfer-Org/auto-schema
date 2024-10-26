import json
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
from file_processor import get_files_structure
from json_to_mdx import generate_mdx

def export_to_json(file_path):
    files_structure = get_files_structure(file_path)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    json_filename = f"schema_{timestamp}.json"
    with open(json_filename, 'w', encoding='utf-8') as json_file:
        json.dump(files_structure, json_file, indent=4)
    return json_filename, files_structure

def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    # doesn't work for folders, you will have to do askopendirectory or smth like that
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("All files", "*.*")])
    if file_path:
        json_filename, files_structure = export_to_json(file_path)
        print(f"JSON schema exported successfully to: {json_filename}")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        # Generate MDX file
        mdx_filename = f"generated_mdx_{timestamp}.mdx"
        generate_mdx(files_structure, mdx_filename)
        print(f"MDX file generated successfully: {mdx_filename}")
    else:
        print("No folder selected. Operation cancelled.")

def main():
    select_file()

if __name__ == "__main__":
    main()
