# Ian Cassidy
# Harmonic Transponder - Discrete Component
# Plotting Input Power Sweep - Extrapolation
# Sept 25, 2026

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

DUT = "MMDL S23"        # Device Name: First 4 chars of part# + month and day fabricated

data_folder = Path(__file__).parent.parent / "data" / "test_processed"
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

# Plot Options (User Input)
measurements = {
    "1": ("Conversion loss", "Conversion Loss (dB)"),
    "2": ("Harmonic Ratio", "Harmonic Ratio (dB)"),
    "3": ("Output Power", "Output Power (dBm)"),
    "4": ("Slope", "Slope (dB/dB)")
}

# Ask calibration
print("\nCalibration:")
print("1 = Calibrated")
print("2 = Uncalibrated")
print("3 = Calibrated vs Uncalibrated")

cal_choice = input("\nChoose: ").strip()

while cal_choice not in ["1", "2", "3"]:
    cal_choice = input("Enter 1, 2, or 3: ").strip()

# Ask measurement type
print("\nMeasurements:")
print("1 = Conversion Loss")
print("2 = Harmonic Ratio")
print("3 = Output Power")
print("4 = Slope")
print("\nEnter any combination.")
print("Examples: 1   12   234   41")

measurement_choice = input("\nChoose: ").strip()

# Allow commas and spaces
measurement_choice = (
    measurement_choice
    .replace(",", "")
    .replace(" ", "")
)

# Remove duplicates while preserving order
measurement_choice = "".join(
    dict.fromkeys(measurement_choice)
)

while (
    not measurement_choice
    or any(x not in measurements for x in measurement_choice)
):
    measurement_choice = input(
        "Enter a combination of 1, 2, 3, and 4: "
    ).strip()

    measurement_choice = (
        measurement_choice
        .replace(",", "")
        .replace(" ", "")
    )

    measurement_choice = "".join(
        dict.fromkeys(measurement_choice)
    )

# Select data
if cal_choice == "1":
    data_sets = [
        ("Calibrated", calibrated_data_set)
    ]

elif cal_choice == "2":
    data_sets = [
        ("Uncalibrated", uncalibrated_data_set)
    ]

else:
    data_sets = [
        ("Calibrated", calibrated_data_set),
        ("Uncalibrated", uncalibrated_data_set)
    ]

# Ask extrapolation
print("\nExtrapolation:")
print("y = Add linear extrapolation")
print("n = No extrapolation")

extrapolation_choice = input("\nChoose: ").strip().lower()

while extrapolation_choice not in ["y", "n"]:
    extrapolation_choice = input("Enter y or n: ").strip().lower()

if extrapolation_choice == "y":
    lower_bound = float(
        input("\nEnter lower bound for extrapolation (dBm): ")
    )

    upper_bound = float(
        input("Enter upper bound for extrapolation (dBm): ")
    )

    while upper_bound <= lower_bound:
        print("Upper bound must be greater than lower bound.")
        lower_bound = float(
            input("Enter lower bound for extrapolation (dBm): ")
        )

        upper_bound = float(
            input("Enter upper bound for extrapolation (dBm): ")
        )

# Create plots
for choice in measurement_choice:
    measurement, ylabel = measurements[choice]

    plt.figure()
    for set_name, data_set in data_sets:
        data = data_set[measurement]
        for harmonic, values in data.items():
            if cal_choice == "3":
                label = f"{set_name} {harmonic}"
            else:
                label = harmonic
                
            plt.plot(Pin, values, marker="o", markersize=4, linewidth=1.5, label=label)

            # Linear extrapolation
            if extrapolation_choice == "y":
                coefficients = np.polyfit(Pin, values, 2)

                fit = np.poly1d(coefficients)

                x_fit = np.linspace(
                    lower_bound,
                    upper_bound,
                    200
                )

                y_fit = fit(x_fit)

                plt.plot(
                x_fit,
                y_fit,
                linestyle="--",
                label=f"{label} {i+1} Fit"
            )

    # Title
    if cal_choice == "1":
        title_calibration = "Calibrated"

    elif cal_choice == "2":
        title_calibration = "Uncalibrated"

    else:
        title_calibration = "Calibrated vs Uncalibrated"

    plt.title(
        f"{title_calibration} {measurement} "
        f"vs Input Power for {DUT}"
    )
    plt.xlabel("Input Power (dBm)")
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.legend()
    plt.show()