#Working code to update alternative names in Pure using the Pure API

import csv
import json
import requests
from datetime import datetime
import os

# Configuration
base_url = "https://api.elsevierpure.com/ws/api"
endpoint = "/external-organizations/"
input_file = "/mnt/c/Users/hlawrenc/API/alt_name/test_01.csv"  # Updated file path
log_file = "update_log.txt"

# Read API key from file
with open(os.path.join("/mnt/c/Users/hlawrenc/API/alt_name/api_key.txt"), "r") as key_file:
    api_key = key_file.read().strip()

# Function to log messages with timestamps
def log_message(message):
    with open(log_file, "a") as log:
        log.write(f"{datetime.now()}: {message}\n")

# Read CSV and update database
with open(input_file, mode='r') as file:
    csv_reader = list(csv.DictReader(file))  # Convert to list to get total count
    total = len(csv_reader)
    for idx, row in enumerate(csv_reader, start=1):
        # Visual progress bar
        bar_length = 40
        filled_length = int(bar_length * idx // total)
        bar = '=' * filled_length + '-' * (bar_length - filled_length)
        print(f"\rProgress: |{bar}| {idx}/{total}", end='')

        if 'uuid' not in row:
            log_message("UUID key is missing in the row, skipping record")
            continue
        
        uuid = row['uuid']
        alternativeNames = row['alternativeNames'].split('|')
        
        # Prepare JSON payload
        payload = {
            "alternativeNames": alternativeNames
        }
        
        # Make PUT request to update the database
        url = f"{base_url}{endpoint}{uuid}"
        headers = {
            "Content-Type": "application/json",
            "api-key": api_key
        }
        response = requests.put(url, headers=headers, data=json.dumps(payload))
        
        # Log the result
        if response.status_code == 200:
            log_message(f"Successfully updated record {uuid}")
        else:
            log_message(f"Failed to update record {uuid}: {response.status_code} {response.text}")

    print()  # Move to next line after progress bar