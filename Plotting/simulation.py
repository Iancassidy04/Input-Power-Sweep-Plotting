# Ian Cassidy
# Harmonic Transponder
# ADS Simulation Data Plotting
# Sept 25 2026

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Find ADS data
data_folder = Path(__file__).parent.parent / "data" / "ADS"
files = list(data_folder.glob("*.txt"))

print("\nADS Simulation Files:")

for i, file in enumerate(files, 1):
    print(f"{i} = {file.name}")

file_choice = int(input("\nChoose TXT file: "))
filename = files[file_choice - 1]

# Read file
with open(filename, "r") as file:
    lines = file.readlines()

# Store data
harmonics = {}
current_harmonic = None
Pin = []

# Read ADS ASCII data
for line in lines:

    line = line.strip()

    if not line:
        continue

    # Find harmonic
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
                Pin.append(pin)

            harmonics[current_harmonic].append(pout)

    except ValueError:
        continue

Pin = np.array(Pin)

# Create plot
plt.figure()

for harmonic, values in harmonics.items():

    values = np.array(values)

    plt.plot(
        Pin,
        values,
        marker="o",
        markersize=4,
        linewidth=1.5,
        label=f"M{harmonic}"
    )

plt.xlabel("Input Power (dBm)")
plt.ylabel("Output Power (dBm)")
plt.title("ADS Harmonic Output Power vs Input Power")
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.show()