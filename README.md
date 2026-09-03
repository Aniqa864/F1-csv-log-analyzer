# 🏎️ F1 CSV Log Analyzer

A Python script that analyzes historical Formula 1 race data (1950–2025) from CSV files and generates a clean, human-readable summary report — covering points leaders, race wins, DNF rates, average position changes, and more.

## 📋 Features

- **Driver Records** — identifies the all-time points leader and the driver with the most race wins
- **Race Performance** — calculates average grid-to-finish position change and average laps completed
- **Reliability Stats** — computes total DNFs (Did Not Finish) and DNF rate as a percentage
- **Constructor & Nationality Insights** — finds the most winning constructor and nationality
- **Dataset Overview** — total race entries, unique races, drivers, and constructors
- Outputs a formatted `.txt` report plus a console summary

## 📁 Project Structure

```
.
├── data/
│   ├── results.csv       # Race results data
│   └── drivers.csv       # Driver details data
├── output/
│   └── f1_summary.txt    # Generated report (created on run)
└── main.py                # Main script
```

## 🔧 Requirements

- Python 3.7+
- [matplotlib](https://matplotlib.org/) (used for the `grid` import)

Install dependencies:

```bash
pip install matplotlib
```

## 📥 Input Data Format

### `data/results.csv`
Expected columns include:

| Column | Description |
|---|---|
| `race_id` | Unique identifier for the race |
| `driver_id` | Unique identifier for the driver |
| `constructor_id` | Unique identifier for the constructor/team |
| `grid` | Starting grid position |
| `position` | Finishing position (or `\N` if DNF) |
| `position_order` | Final classified position order |
| `points` | Points scored in the race |
| `laps` | Number of laps completed |

### `data/drivers.csv`
Expected columns include:

| Column | Description |
|---|---|
| `driver_id` | Unique identifier for the driver |
| `givenName` | Driver's first name |
| `familyName` | Driver's last name |
| `nationality` | Driver's nationality |

## ▶️ Usage

1. Place your `results.csv` and `drivers.csv` files inside the `data/` folder.
2. Run the script:

```bash
python main.py
```

3. The report will be generated at `output/f1_summary.txt`, and a summary will also print to the console.

## 📊 Sample Output

```
================================================
FORMULA 1 HISTORICAL DATA REPORT
1950 - 2025  | All Seasons
================================================

DATASET OVERVIEW
-----------------------------------
  Total race entries   : 26,000
  Total races          : 1,100
  Unique drivers       : 860
  Unique constructors  : 210

DRIVER RECORDS
-----------------------------------
  All-time points leader : Lewis Hamilton
  Their total points     : 4,639.5
  Most race wins         : Lewis Hamilton (105 wins)

RACE PERFORMANCE
-----------------------------------
  Avg grid-to-finish change : +0.42 places
  Avg laps completed        : 55.3

RELIABILITY
-----------------------------------
  Total DNFs  : 5,200
  DNF rate    : 20.0%

CONSTRUCTOR & NATIONALITY
-----------------------------------
  Most winning constructor ID : 6 (243 wins)
  Most winning nationality    : British (312 wins)
```

## 🛠️ How It Works

1. **Load Data** — reads `results.csv` and `drivers.csv` into memory using Python's built-in `csv.DictReader`
2. **Build Lookups** — maps `driver_id` to full names and nationalities for fast reference
3. **Analyze** — computes points totals, wins, position gains, DNF rate, and other aggregate statistics
4. **Report** — writes a formatted text report to `output/f1_summary.txt` and prints key highlights to the console
