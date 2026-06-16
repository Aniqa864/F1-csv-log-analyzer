import os
import csv

# Project configuration and file paths
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


# Implementing a function to safely convert values to floats, returning a default value if conversion fails
def safe_float(value, default=0.0):
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def analyze(results, driver_lookup, nationality_lookup):

    # Calculate total points for each driver
    points_per_driver = {}
    for row in results:
        d_id = row["driver_id"]
        pts  = safe_float(row["points"])
        points_per_driver[d_id] = points_per_driver.get(d_id, 0.0) + pts

    top_id     = max(points_per_driver, key=points_per_driver.get)
    top_name   = driver_lookup.get(top_id, f"Driver #{top_id}")
    top_points = round(points_per_driver[top_id], 1)