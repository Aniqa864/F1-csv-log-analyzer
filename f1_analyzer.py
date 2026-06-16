import os
import csv

INPUT_RESULTS = "data/results.csv"
INPUT_DRIVERS = "data/drivers.csv"
OUTPUT_FILE = "output/f1_summary.txt"


def read_csv(file_path):
    row = []
    with open(filepath, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            row.append(line)
    print(f"Loaded {len(row)} rows from {file_path}")
    return row