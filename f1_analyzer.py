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
def build_driver_lookup(drivers):
    lookup = {}
    for row in drivers:
        driver_id = row["driver_id"]
        full_name = row["givenName"] + " " + row["familyName"]
        lookup[driver_id] = full_name
    return lookup


# Implementing a function to create a lookup dictionary for drivers based on their nationalities
def build_nationality_lookup(drivers):
    lookup = {}
    for row in drivers:
        lookup[row["driver_id"]] = row["nationality"]
    return lookup


# Implementing a function to safely convert values to floats, returning a default value if conversion fails
def safe_int(value, default=0.0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def analyze(results, driver_lookup):

    # Calculate total points for each driver
    points_per_driver = {}
    for row in results:
        d_id = row["driver_id"]
        pts  = safe_int(row["points"])
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
            grid = safe_int(row["grid"])
            finish = safe_int(row["position_order"])
            if grid > 0 and finish > 0:
                position_gains.append(grid - finish)
        except (ValueError):
            pass
    
    avg_gain = round(sum(position_gains)/len(position_gains), 2) if position_gains else 0


    # Calculate DNF (Did Not Finish) rate
    dnf_count = sum(
        1 for row in results
        if row["position"].strip() in ("\\N", "", "0")
    )

    dnf_rate = round((dnf_count / len(results)) * 100, 1) if results else 0


    # Calculate constructor wins
    constructor_wins = {}
    for row in results:
        if safe_int(row["position_order"]) == 1:
            c_id = row["constructor_id"]
            constructor_wins[c_id] = constructor_wins.get(c_id, 0) + 1

    top_constructor_id    = max(constructor_wins, key=constructor_wins.get) if constructor_wins else None
    top_constructor_wins  = constructor_wins.get(top_constructor_id, 0)


    # Calculate nationality wins
    nationality_wins = {}
    for row in results:
        if safe_int(row["position_order"]) == 1:
            d_id        = row["driver_id"]
            nationality = build_nationality_lookup.get(d_id, "Unknown")
            nationality_wins[nationality] = nationality_wins.get(nationality, 0) + 1

    top_nationality       = max(nationality_wins, key=nationality_wins.get) if nationality_wins else "Unknown"
    top_nationality_wins  = nationality_wins.get(top_nationality, 0)


    # Unique counts
    total_races        = len(set(row["race_id"]    for row in results))
    total_drivers      = len(set(row["driver_id"]  for row in results))
    total_constructors = len(set(row["constructor_id"] for row in results))


    # Average laps completed
    laps = [safe_int(row["laps"]) for row in results if safe_int(row["laps"]) > 0]
    avg_laps = round(sum(laps) / len(laps), 1) if laps else 0

    return {
        "total_entries"        : len(results),
        "total_races"          : total_races,
        "total_drivers"        : total_drivers,
        "total_constructors"   : total_constructors,
        "top_name"             : top_name,
        "top_points"           : top_points,
        "most_wins_name"       : most_wins_name,
        "most_wins_count"      : most_wins_count,
        "avg_gain"             : avg_gain,
        "dnf_count"            : dnf_count,
        "dnf_rate"             : dnf_rate,
        "top_constructor_id"   : top_constructor_id,
        "top_constructor_wins" : top_constructor_wins,
        "top_nationality"      : top_nationality,
        "top_nationality_wins" : top_nationality_wins,
        "avg_laps"             : avg_laps,
    }

# Implementing a function to write the analysis report to a specified file path
def write_report(stats, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("=" * 48 + "\n")
        f.write("FORMULA 1 HISTORICAL DATA REPORT\n")
        f.write("1950 - 2025  | All Seasons\n")
        f.write("=" * 48 + "\n\n")

        f.write("DATASET OVERVIEW\n")
        f.write("-" * 35 + "\n")
        f.write(f"  Total race entries   : {stats['total_entries']:,}\n")
        f.write(f"  Total races          : {stats['total_races']:,}\n")
        f.write(f"  Unique drivers       : {stats['total_drivers']:,}\n")
        f.write(f"  Unique constructors  : {stats['total_constructors']:,}\n\n")

        f.write("DRIVER RECORDS\n")
        f.write("-" * 35 + "\n")
        f.write(f"  All-time points leader : {stats['top_name']}\n")
        f.write(f"  Their total points     : {stats['top_points']:,}\n")
        f.write(f"  Most race wins         : {stats['most_wins_name']}"
                f" ({stats['most_wins_count']} wins)\n\n")

        f.write("RACE PERFORMANCE\n")
        f.write("-" * 35 + "\n")
        f.write(f"  Avg grid-to-finish change : {stats['avg_gain']:+.2f} places\n")
        f.write(f"  Avg laps completed        : {stats['avg_laps']}\n\n")

        f.write("RELIABILITY\n")
        f.write("-" * 35 + "\n")
        f.write(f"  Total DNFs  : {stats['dnf_count']:,}\n")
        f.write(f"  DNF rate    : {stats['dnf_rate']}%\n\n")

        f.write("CONSTRUCTOR & NATIONALITY\n")
        f.write("-" * 35 + "\n")
        f.write(f"  Most winning constructor ID : {stats['top_constructor_id']}"
                f" ({stats['top_constructor_wins']} wins)\n")
        f.write(f"  Most winning nationality    : {stats['top_nationality']}"
                f" ({stats['top_nationality_wins']} wins)\n")

    print(f"Report written to {file_path}")


def main():
    print("F1 CSV Log Analyzer — 1950 to 2025")
    print("-" * 38)

    for path in (INPUT_RESULTS, INPUT_DRIVERS):
        if not os.path.exists(path):
            print(f"  ERROR: Missing file → {path}")
            return

    results = read_csv(INPUT_RESULTS)
    drivers = read_csv(INPUT_DRIVERS)

    driver_lookup      = build_driver_lookup(drivers)
    nationality_lookup = build_nationality_lookup(drivers)

    stats = analyze(results, driver_lookup, nationality_lookup)
    write_report(stats, OUTPUT_FILE)

    print(f"\n── Key results ──────────────────────")
    print(f"  Points leader : {stats['top_name']} ({stats['top_points']} pts)")
    print(f"  Most wins     : {stats['most_wins_name']} ({stats['most_wins_count']} wins)")
    print(f"  DNF rate      : {stats['dnf_rate']}%")
    print(f"  Report saved  : {OUTPUT_FILE}")
    

if __name__ == "__main__":
    main()