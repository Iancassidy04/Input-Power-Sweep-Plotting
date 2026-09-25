# Harmonic Transponder

Python scripts for testing and analyzing a diode-based harmonic transponder.

## Overview

This project is being developed to characterize the harmonic generation performance of discrete diode harmonic transponders.

The response of the device is measured as input power is swept and analyzing the fundamental and harmonic output powers.

## Current Functionality

The repository currently contains plotting scripts for measured input power sweep data.

The plots include:

- Conversion Loss
- Harmonic Ratio
- Output Power
- Harmonic Slope
- Calibrated vs. uncalibrated measurements
- Polynomial extrapolation

Measurement data is currently stored as CSV files in the `data` folder.

## Repository Structure

```text
harmonic-transponder/
├── data/
│   └── *.csv
├── plotting/
│   ├── plot_extrapolation.py
│   ├── plot_harmonics.py
│   └── ...
└── README.md
Data
```

CSV files contain the input power sweep and measured harmonic data.

The data includes calibrated and uncalibrated measurements for the fundamental and harmonics.

# Future Work

The next stage of the project is to automate the measurement process.

An automated input power sweep will be developed using an Agilent E4422B ESG signal generator and an Agilent N9010A EXA signal analyzer.

## User Specified Parameters

- Fundamental frequency
- Starting input power
- Final input power
- Input power step
- Number of harmonics
- Resolution bandwidth
- Analyzer span

## Example:

- Fundamental Frequency: 525 MHz
- Input Power:           -30 to +10 dBm
- Power Step:            0.5 dB
- Harmonics:             f0 - 4f0
- Resolution Bandwidth:  1 kHz
- Span:                  10 kHz

For each input power level, the signal analyzer will perform a peak search at the fundamental frequency and its harmonics:

- f0
- 2f0
- 3f0
- 4f0

The input power and measured output powers will then be saved to a raw data file.

## Planned Data Processing

The raw instrument data will be processed automatically to calculate:

- Conversion Loss
- Harmonic Ratio
- Harmonic Slope

From:
- Fundamental output power
- 2nd harmonic output power
- 3rd harmonic output power
- 4th harmonic output power

for both the DUT and a THRU test board.

## Planned Repository Structure

```text
harmonic-transponder/
├── data/
│   ├── raw/
│   └── processed/
├── automation/
│   └── power_sweep.py
├── processing/
├── plotting/
└── README.md
```

## End Goal

The final system will:

- Configure the signal generator and signal analyzer
- Sweep the input power
- Measure the fundamental and harmonic output powers
- Save the raw measurement data
- Process and calibrate the data
- Calculate harmonic performance metrics
- Generate plots for analysis

This will provide a repeatable measurement and analysis workflow for characterizing discrete-component harmonic transponders.
