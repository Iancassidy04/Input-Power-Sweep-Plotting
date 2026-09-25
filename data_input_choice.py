# Ian Cassidy
# Harmonic Transponder - Discrete Component
# Plotting Input Power Sweep - Diode only
# Sept 25, 2026

import pandas as pd
import matplotlib.pyplot as plt

DUT = "MMDL S23"        # Device Name: First 4 chars of part# + month and day fabricated

filename = r"C:\Users\ianbc\OneDrive - University of Vermont\Saw Research\IAN_SAW\Code\Input Power Sweep Plotting\2026_09_24_PIN_SWEEP_MMDLS23.csv"
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

            plt.plot(
                Pin,
                values,
                marker="o",
                markersize=4,
                linewidth=1.5,
                label=label
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