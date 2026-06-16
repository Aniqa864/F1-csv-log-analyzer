import os
import csv

#Project configuration and file paths
INPUT_RESULTS = "data/results.csv"
INPUT_DRIVERS = "data/drivers.csv"
OUTPUT_FILE = "output/f1_summary.txt"


# Implementing a CSV reader function to load data from the specified file path
def read_csv(file_path):
    row = []
    with open(filepath, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            row.append(line)
    print(f"Loaded {len(row)} rows from {file_path}")
    return row


# Implementing a function to create a lookup dictionary for drivers based on their IDs
def driver_lookup(drivers):
    lookup = {}
    for row in drivers:
        driver_id = row["driver_id"]
        full_name = row["givenName"] + " " + row["familyName"]
        lookup[driver_id] = full_name
    return lookup


# Implementing a function to create a lookup dictionary for drivers based on their nationalities
def nationality_lookup(drivers):
    lookup = {}
    for row in drivers:
        lookup[row["driver_id"]] = row["nationality"]
    return lookup


