from tkinter import filedialog
from datetime import datetime
import uuid
import json
import csv
import re


# Function to generate a unique ID (UUID)
def generate_unique_id():
    return str(uuid.uuid4())


# Function to get the current timestamp
def get_current_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Function to validate if an email is valid
def is_valid_email(email):
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_regex, email) is not None


# Function to save data to CSV (dynamic for any data)
def save_to_csv(file_path, headers, data):
    with open(file_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for row in data:
            writer.writerow(row)


# Function to load data from CSV
def load_from_csv(file_path):
    data = []
    try:
        with open(file_path, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        pass  # If no file exists, return an empty list
    return data


# Function to refresh dynamic data table in the GUI
def refresh_table(tree, data_dict):
    for row in tree.get_children():
        tree.delete(row)
    for key, values in data_dict.items():
        row_data = (key,) + tuple(values.values())
        tree.insert("", "end", values=row_data)


# Function to export data to JSON
def export_data_to_json(data, filename):
    timestamp = datetime.now().isoformat()
    timestamp = timestamp.replace(":", "-").replace(".", "-")
    json_filename = f"{timestamp}_{filename}.json"

    with open(json_filename, "w") as json_file:
        json.dump(data, json_file, indent=4)

    print(f"Exported data to {json_filename}.")


# Function to import data from a JSON file
def import_data_from_json():
    # Open file dialog to select the JSON file
    filename = filedialog.askopenfilename(
        title="Select a JSON file",
        filetypes=(("JSON files", "*.json"), ("All files", "*.*")),
    )

    if not filename:
        raise FileNotFoundError("No file was selected")

    try:
        # Open and load the JSON file
        with open(filename, "r") as json_file:
            data = json.load(json_file)
            return data  # Return the imported data
    except json.JSONDecodeError:
        raise ValueError("The selected file is not a valid JSON.")
    except Exception as e:
        raise RuntimeError(f"An error occurred while importing data: {e}")
