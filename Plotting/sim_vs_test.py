# Ian Cassidy
# Harmonic Transponder
# Test Data vs ADS Simulation
# Sept 25 2026

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

DUT = "MMDL S23"        # Device Name: First 4 chars of part# + month and day fabricated


# Find ADS data

def choose_data(ftype, sub_data):

    data_folder = Path(__file__).parent.parent / "data" / sub_data
    files = list(data_folder.glob(ftype))

    print("\n{sub_data} Simulation Files:")

    for i, file in enumerate(files, 1):
        print(f"{i} = {file.name}")

    file_choice = int(input("\nChoose file: "))
    return files[file_choice - 1]

filename_ads = choose_data("*.txt", "ADS")
filename_test = choose_data("*.csv", "test_processed")

from linear_extrapolation import plot_test
from simulation import plot_sim

plot_test(filename_test)
plot_sim(filename_ads)
