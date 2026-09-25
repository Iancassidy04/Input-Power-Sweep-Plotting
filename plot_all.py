# Ian Cassidy
# Harmonic Transponder - Discrete Component
# Plotting Input Power Sweep - Extrapolation
# Sept 25, 2026

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


DUT = "MMDL S23"        # Device Name: First 4 chars of part# + month and day fabricated

# Select data file from repo options
data_folder = Path(__file__).parent / "data"
files = list(data_folder.glob("*.csv"))

print("\nCSV Files:")

for i, file in enumerate(files, 1):
    print(f"{i} = {file.name}")

file_choice = int(input("\nChoose CSV: "))
filename = files[file_choice - 1]
df = pd.read_csv(filename)

# Data Dictionarys
calibrated_data_set = {
    "Conversion loss": {},
    "Output Power": {},
    "Harmonic Ratio": {},
    "Slope": {}
}

uncalibrated_data_set = {
    "Conversion loss": {},
    "Output Power": {},
    "Harmonic Ratio": {},
    "Slope": {}
}

Pin = df["Pin"]

# Organize CSV Columns
for column in df.columns:
    if "_" not in column:
        continue

    parts = column.split("_")
    calibration = parts[0]
    harmonic = parts[1]
    measurement = parts[2]

    if calibration == "c":
        data_set = calibrated_data_set

    elif calibration == "u":
        data_set = uncalibrated_data_set

    else:
        continue

    if measurement == "CL":
        data_set["Conversion loss"][harmonic] = df[column]

    elif measurement == "P":
        data_set["Output Power"][harmonic] = df[column]

    elif measurement == "HR":
        data_set["Harmonic Ratio"][harmonic] = df[column]

    elif measurement == "S":

        if harmonic in ["M2", "M3"]:         # Only M2 and M3
            data_set["Slope"][harmonic] = df[column]

# Plot Options
measurements = {
    "1": ("Conversion loss", "Conversion Loss (dB)"),
    "2": ("Harmonic Ratio", "Harmonic Ratio (dB)"),
    "3": ("Output Power", "Output Power (dBm)"),
    "4": ("Slope", "Slope (dB/dB)")
}

# Ask extrapolation
print("\nExtrapolation:")
print("y = Add polynomial extrapolation")
print("n = No extrapolation")

extrapolation_choice = input("\nChoose: ").strip().lower()

while extrapolation_choice not in ["y", "n"]:
    extrapolation_choice = input("Enter y or n: ").strip().lower()

if extrapolation_choice == "y":
    lower_bound = float(input("\nEnter lower bound for extrapolation (dBm): "))
    upper_bound = float(input("Enter upper bound for extrapolation (dBm): "))

    while upper_bound <= lower_bound:
        print("Upper bound must be greater than lower bound.")
        lower_bound = float(input("Enter lower bound for extrapolation (dBm): "))
        upper_bound = float(input("Enter upper bound for extrapolation (dBm): "))

# Data Sets to Plot
data_set_options = [
    ("Calibrated", calibrated_data_set),
    ("Uncalibrated", uncalibrated_data_set),
    ("Calibrated vs Uncalibrated", None)
]

# Create plots
for plot_type, data_set in data_set_options:
    for choice in measurements:
        measurement, ylabel = measurements[choice]

        plt.figure()

        if plot_type != "Calibrated vs Uncalibrated":           # Calibrated or Uncalibrated
            data = data_set[measurement]
            for harmonic, values in data.items():

                # Remove NaN values
                x = np.array(Pin, dtype=float)
                y = np.array(values, dtype=float)

                valid = np.isfinite(x) & np.isfinite(y)

                x = x[valid]
                y = y[valid]

                label = f"{plot_type} {harmonic}"

                plt.plot(x, y, marker="o", markersize=4, linewidth=1.5, label=label)

                # Polynomial extrapolation
                if extrapolation_choice == "y" and len(x) >= 3:

                    coefficients = np.polyfit(x, y, 2)
                    fit = np.poly1d(coefficients)

                    x_fit = np.linspace(lower_bound, upper_bound, 200)
                    y_fit = fit(x_fit)

                    plt.plot(x_fit, y_fit, linestyle="--", linewidth=1.5, label=f"{label} Fit")

        else:
            for i in range(2):
                data = calibrated_data_set[measurement] if i == 1 else uncalibrated_data_set[measurement]
                cal = "Calibrated" if i == 1 else "Uncalibrated"

            for harmonic, values in data.items():

                x = np.array(Pin, dtype=float)
                y = np.array(values, dtype=float)

                valid = np.isfinite(x) & np.isfinite(y)

                x = x[valid]
                y = y[valid]

                label = f"{cal} {harmonic}"

                plt.plot(x, y, marker="o", markersize=4, linewidth=1.5, label=label)

                if extrapolation_choice == "y" and len(x) >= 3:

                    coefficients = np.polyfit(x, y, 2)
                    fit = np.poly1d(coefficients)

                    x_fit = np.linspace(lower_bound, upper_bound, 200)

                    y_fit = fit(x_fit)

                    plt.plot(x_fit, y_fit, linestyle="--", linewidth=1.5, label=f"{cal} {harmonic} Fit")

        # Title
        plt.title(
            f"{plot_type} {measurement} "
            f"vs Input Power for {DUT}"
        )
        plt.xlabel("Input Power (dBm)")
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.legend()
    plt.show()