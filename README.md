# Harmonic Transponder - Discrete Component

Python scripts for processing and analyzing input power sweeps on a diode-based harmonic transponder.

## Purpose

This project plots measured harmonic transponder data as a function of input power and compares calibrated and uncalibrated measurements.

The script can plot:

- Conversion Loss
- Harmonic Ratio
- Output Power
- Harmonic Slope

Measurements are available for:

- Fundamental (M1)
- 2nd Harmonic (M2)
- 3rd Harmonic (M3)


## Data

Place CSV measurement files in the `data` folder:

```text
project/
├── data/
│   ├── measurement1.csv
│   ├── measurement2.csv
│   └── ...
├── plotting_script.py
└── README.md
