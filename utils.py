import json
import re

import csv

def csv_to_dict_list(file_path):
    """
    Reads a CSV file and returns a list of dictionaries.
    
    Each dictionary corresponds to a row in the CSV file, where the keys are the column headers.
    
    Args:
        file_path (str): The path to the CSV file.
    
    Returns:
        list of dict: List containing a dictionary for each row.
    """
    with open(file_path, mode='r', newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        return [row for row in reader]

def read_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)
    


def write_json(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def parse_tag_response( tag_pattern, text: str):
    responses = re.findall(tag_pattern, text, re.DOTALL)
    responses = [t.strip() for t in responses]
    return " ".join(responses)