🏎️ F1 CSV Log Analyzer
A Python-based data analysis tool that processes historical Formula 1 race results from CSV files and generates a concise summary report containing driver records, race performance, reliability statistics, constructor wins, and nationality-based statistics.

The project is designed to demonstrate practical Python skills including CSV processing, dictionaries, data aggregation, file handling, error handling, and report generation.

📌 Features
📂 Reads Formula 1 data from CSV files
👨‍✈️ Calculates the all-time points leader
🏆 Identifies the driver with the most race wins
📈 Calculates the average grid-to-finish position change
🚨 Calculates total DNFs (Did Not Finish) and DNF rate
🏁 Identifies the constructor with the most wins
🌍 Identifies the nationality with the most race wins
👥 Counts unique drivers and constructors
🛣️ Calculates average laps completed
📄 Generates a formatted text report
🛡️ Includes basic handling for missing or invalid numeric values

📁 Project Structure
f1-csv-log-analyzer/
│
├── data/
│   ├── results.csv
│   └── drivers.csv
│
├── output/
│   └── f1_summary.txt
│
├── main.py
│
└── README.md

📊 Data
The analyzer expects two CSV files inside the data/ directory.

results.csv
Contains race-result information such as:

race_id
driver_id
constructor_id
grid
position
position_order
points
laps

drivers.csv
Contains driver information such as:

driver_id
givenName
familyName
nationality

The driver data is used to convert driver IDs into full names and determine the nationality associated with each driver.

⚙️ How It Works
The program follows a simple analysis pipeline:

CSV Files
   │
   ▼
Read Data
   │
   ▼
Build Driver Lookups
   │
   ▼
Analyze Race Results
   │
   ├── Points
   ├── Wins
   ├── Position Gain
   ├── DNFs
   ├── Constructor Wins
   ├── Nationality Wins
   └── Average Laps
   │
   ▼
Generate Statistics
   │
   ▼
Write f1_summary.txt

🚀 Getting Started
1. Clone the repository
git clone https://github.com/Aniqa864/F1-csv-log-analyzer.git
cd F1-csv-log-analyzer

2. Add the data files
Place the required CSV files in:

data/results.csv
data/drivers.csv

3. Run the analyzer
python main.py

The program will check that both input files exist before starting the analysis.

💻 Example Console Output
F1 CSV Log Analyzer — 1950 to 2025
--------------------------------------
Loaded 26000 rows from data/results.csv
Loaded 860 rows from data/drivers.csv
Report written to output/f1_summary.txt

── Key results ──────────────────────
  Points leader : Lewis Hamilton (.... pts)
  Most wins     : Lewis Hamilton (.... wins)
  DNF rate      : ....%
  Report saved  : output/f1_summary.txt

The exact results depend on the CSV dataset being analyzed.

📄 Generated Report
The analyzer creates:

output/f1_summary.txt

The report contains several sections.

Dataset Overview
Total race entries
Total races
Unique drivers
Unique constructors
Driver Records
All-time points leader
Total points
Driver with the most race wins
Race Performance
Average grid-to-finish change
Average laps completed
Reliability
Total DNFs
DNF percentage
Constructor & Nationality
Constructor with the most wins
Nationality with the most wins

🧮 Calculations
Driver Points
Points are accumulated for every driver across all race results:

points_per_driver[d_id] = points_per_driver.get(d_id, 0) + pts

The driver with the highest total is selected as the points leader.

Race Wins
A race is counted as a win when:

position_order == 1

Grid-to-Finish Change
The position change is calculated as:

Grid Position - Finishing Position

For example:

Started: 12th
Finished: 5th

Gain = 12 - 5 = +7 places

DNF Rate
A result is treated as a DNF when the position field is:

\N
""
"0"

The DNF rate is then calculated as:

DNF Rate = (DNFs / Total Results) × 100

🛠️ Technologies Used
Python 3
csv — reading CSV data
os — file and directory handling
No external Python packages are required to run the analyzer.

📚 Python Concepts Demonstrated
This project demonstrates several fundamental Python programming concepts:

Functions
Loops
Dictionaries
List comprehensions
Conditional statements
Exception handling
File I/O
CSV parsing
Data aggregation
Dictionary lookups
Basic statistical calculations
Modular program structure

🔮 Possible Future Improvements
Some ideas for extending the project:

Add season-by-season analysis
Add constructor names instead of constructor IDs
Generate charts using matplotlib
Export reports to CSV or JSON
Add command-line arguments for custom input files
Calculate podium finishes
Analyze fastest laps
Compare drivers across different seasons
Add driver championship standings
Create an interactive dashboard
Add automated tests with pytest

⚠️ Notes
The report header currently describes the dataset as covering 1950–2025. The actual statistics depend entirely on the contents of the supplied CSV files.

For accurate results, make sure the CSV files contain the expected columns and compatible Formula 1 race-result data.

🏁 Project Goal
F1 CSV Log Analyzer is a lightweight Python project for turning raw Formula 1 race-result CSV data into useful historical statistics.

It provides a practical example of how Python can be used to transform structured data into a readable analytical report.

Built with Python 🐍 | Powered by F1 data 🏎️
