# Ian Cassidy
# Harmonic Transponder
# Test Data vs ADS Simulation
# Sept 25 2026

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd

DUT = "MMDL S23"        # Device Name: First 4 chars of part# + month and day fabricated

# Choose Data
def choose_data(ftype, sub_data):

    data_folder = Path(__file__).parent.parent / "data" / sub_data
    files = list(data_folder.glob(ftype))

    print(f"\n{sub_data} Files:")

    for i, file in enumerate(files, 1):
        print(f"{i} = {file.name}")

    file_choice = int(input("\nChoose file: "))
    return files[file_choice - 1]

filename_ads = choose_data("*.txt", "ADS")
filename_test = choose_data("*.csv", "test_processed")

# Read Test Data
df = pd.read_csv(filename_test)
Pin_test = df["Pin"]

# Measurements
measurements = {
    "1": ("Conversion loss", "Conversion Loss (dB)", "_CL"),
    "2": ("Harmonic Ratio", "Harmonic Ratio (dB)", "_HR"),
    "3": ("Output Power", "Output Power (dBm)", "_P"),
    "4": ("Slope", "Slope (dB/dB)", "_S")
}

# Select Measurement Type
filename = filename_ads.name

if "_CL" in filename:
    measurement = measurements["1"]

elif "_HR" in filename:
    measurement = measurements["2"]

elif "_P" in filename:
    measurement = measurements["3"]

elif "_S" in filename:
    measurement = measurements["4"]

else:
    print("No test found. File must be named with\n Use _CL, _HR, _P, or _S to denote data type in filename.")
    exit()

measurement_name = measurement[0]
ylabel = measurement[1]
measurement_code = measurement[2]

# Find Test Data Columns
test_columns = []

for column in df.columns:
    if column.startswith("c_") and measurement_code in column:
        # Ignore M1 slope
        if measurement_code == "_S" and "M1" in column:
            continue

        test_columns.append(column)

# Read ADS Data
harmonics = {}
current_harmonic = None

Pin_ads = []

with open(filename_ads, "r") as file:
    lines = file.readlines()

for line in lines:
    line = line.strip()
    if not line:
        continue

    # Find harmonic number
    if "plot_vs" in line:

        start = line.find("Pdbm[") + 5
        end = line.find("]", start)
        current_harmonic = int(line[start:end])
        harmonics[current_harmonic] = []

        continue

    # Read data
    try:
        values = line.split()
        if len(values) == 2:

            pin = float(values[0])
            pout = float(values[1])

            if current_harmonic == 1:
                Pin_ads.append(pin)

            harmonics[current_harmonic].append(pout)

    except ValueError:
        continue

Pin_ads = np.array(Pin_ads)

# Create Plot
plt.figure()

max_M = min(len(harmonics.items()), len(test_columns))

# Plot ADS
M_count = 0

for harmonic, values in harmonics.items():
    M_count += 1
    if M_count > max_M:
        break
    else:
        values = np.array(values)

        plt.plot(Pin_ads, values, linestyle="--", linewidth=1.5, label=f"ADS M{harmonic}")

# Plot Test data
M_count = 0
for column in test_columns:
    M_count += 1
    if M_count > max_M:
        break
    else:
        # Get harmonic number
        parts = column.split("_")
        harmonic = parts[1]

        plt.plot(Pin_test, df[column], marker="o", markersize=4, linewidth=1.5, label=f"Test {harmonic}")

# Plot Settings
plt.title(f"{measurement_name} vs Input Power for {DUT}")
plt.xlabel("Input Power (dBm)")
plt.ylabel(ylabel)
plt.grid(True)
plt.legend()
plt.show()