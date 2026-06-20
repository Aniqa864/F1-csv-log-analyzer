import os
import csv

from matplotlib.pyplot import grid

# Project configuration and file paths
INPUT_RESULTS = "data/results.csv"
INPUT_DRIVERS = "data/drivers.csv"
OUTPUT_FILE = "output/f1_summary.txt"


# Implementing a CSV reader function to load data from the specified file path
def read_csv(file_path):
    row = []
    with open(file_path, newline="", encoding="utf-8") as csvfile:
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

    # Calculate total wins for each driver
    wins_per_driver = {}
    for row in results:
        if safe_int(row["position_order"]) == 1:
            d_id = row["driver_id"]
            wins_per_driver[d_id] = wins_per_driver.get(d_id, 0) + 1

    most_wins_id    = max(wins_per_driver, key=wins_per_driver.get) if wins_per_driver else None
    most_wins_name  = driver_lookup.get(most_wins_id, "Unknown") if most_wins_id else "Unknown"
    most_wins_count = wins_per_driver.get(most_wins_id, 0)


    # Calculate average position gain for each driver
    position_gains = []
    for row in results:
        try:
            grid = int(row["grid"])
            finish = int(row["position_order"])
            if grid > 0 and finish > 0:
                position_gains.append((grid - finish, row["driver_id"]))
        except (ValueError, TypeError):
            pass
    
    avg_position_gain = round(sum(position_gains)/len(position_gains), 2) if position_gains else 0


    # Calculate DNF (Did Not Finish) rate
    dnf_count = 0
    for row in results:
        pos = row["position"]
        if pos in ("\\N", "0", ""):
            dnf_count += 1

    dnf_rate = round((dnf_count / len(results)) * 100, 1) if results else 0


    # Calculate nationality counts 
    nationality_counts = {}
    for row in results:
        driver_id = row["driver_id"]
        name = driver_lookup.get(driver_id, "Unknown")
        nationality_counts[name] = nationality_counts.get(name, 0) + 1


    # Calculate fastest lap speeds
    speeds = []
    for row in results:
        try:
            speed = float(row["fastestLapSpeed"])
            if speed > 0:
                speed.append(speed)
        except (ValueError):
            pass

    max_speed = round(max(speeds),2) if speeds else 0
    avg_speed = round(sum(speeds)/len(speeds),2) if speeds else 0


    # Calculate total races in the dataset
    race_ids = set()
    for row in results:
        race_ids.add(row["race_id"])
    total_races = len(race_ids)

    return {
        "total_entries": len(results),
        "total_races": total_races,
        "top_driver_name": top_name,
        "top_driver_points": top_points,
        "avg_position_change": avg_position_gain,
        "dnf_count" : dnf_count,
        "dnf_rate": dnf_rate,
        "max_speed": max_speed,
        "avg_speed": avg_speed,
    }


def write_report(stats, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("=" * 45 + "\n")
        f.write("FORMULA 1 HISTORICAL DATA REPORT\n")
        f.write("=" * 45 + "\n\n")

        f.write(f"Total race entries analyzed: {stats['total_entries']:,}\n")
        f.write(f"Total races in dataset     : {stats['total_races']:,}\n\n")

        f.write("PERFORMANCE HIGHLIGHTS:\n")
        f.write("-" * 35 + "\n")
        f.write(f"All-time points leader                : {stats['top_driver_name']}\n")
        f.write(f"Their total points                    : {stats['top_driver_points']:,}\n")
        f.write(f"Average grid to finish position change: {stats['avg_position_change']:+.2f}\n")

        f.write("RELIABILITY METRICS:\n")
        f.write("-" * 35 + "\n")
        f.write(f"Total DNFs (Did Not Finish): {stats['dnf_count']:,}\n")
        f.write(f"DNF rate                   : {stats['dnf_rate']}%\n\n")

        f.write("SPEED METRICS:\n")
        f.write("-" * 35 + "\n")
        f.write(f"Maximum recorded fastest lap speed: {stats['max_speed']}km/h\n")
        f.write(f"Average fastest lap speed         : {stats['avg_speed']}km/h\n")

    print(f"Report written to {file_path}")