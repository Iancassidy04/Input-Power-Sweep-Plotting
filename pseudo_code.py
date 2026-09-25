# Ian Cassidy
# Harmonic Transponder - Discrete Component
# Plotting Input Power Sweep - Diode only
# Sept 25, 2026

read csv

columns named: c_M1_CL c_M2_CL	c_M3_CL  c_M2_HR	c_M3_HR  c_M1_P	c_M2_P	c_M3_P  c_M1_S	c_M2_S	c_M3_S  u_M1_CL	u_M2_CL	u_M3_CL	u_M2_HR	u_M3_HR	u_M1_P	u_M2_P	u_M3_P		u_M1_S	u_M2_S	u_M3_S

DUT = "MMDL S23"

"Pin" = Input Power
calibrated_data_set = dictionary{ 
    "Conversion loss": [M1, M2, M3],
    "Output Power": [M1, M2, M3],
    "Harmonic Ratio": [M1, M2, M3],
    "Slope": [M2, M3]

}

uncalibrated_data_set = dictionary{ 
    "Conversion loss": [M1, M2, M3],
    "Output Power": [M1, M2, M3],
    "Harmonic Ratio": [M1, M2, M3],
    "Slope": [M2, M3]

}

for things read that contain "c" and "_"
    In calibrated_data_set add:
    If contains "CL":
        order M1 M2 M3 to Conversion loss list
    If contains "P"
    add M1,2,3 to Power list
    if contains "HR"
        add M1 M2 M3 to harmonic ratio list
    If contains S
        ad M23 to slope list

for things read that contain "u" and "_"
    In uncalibrated_data_set add:
    If contains "CL":
        order M1 M2 M3 to Conversion loss list
    If contains "P"
    add M1,2,3 to Power list
    if contains "HR"
        add M1 M2 M3 to harmonic ratio list
    If contains S
        ad M23 to slope list

Create dictionarry of labels associated with plots:

Input choice: Title appendage, legend apepndage
Plotting = {11: None, None,
 12: "Un", None,
 13: "Uncalibrated vs",
 21: "Conv...", "CL"
 22: " HR... ", "HR"
 23: "Ouptut Power...", "P out"
 24: "Slope", "S"p
 31: None, None
 32: "Extrapolated"

}

ask user what things they want plotted give options 1 through N space with commas, plot all that are inputted 
options include: 
first: cal, uncal, cal vs uncal (11, 12, 13)
then, ask CL, HR, P, S, or a combination: 1 or 12 or 234 of 14 or even 41 (no order) (plot seperatle) (21, 22, 23, 24)
then ask extrapolation (y/n) (25)
if extrapoltion ask lowerbound upper bound input :L , H

plot(selected)
plt.title("{Choice 3} {Choice1}calibrated {choice(s)(vs vs vs) 2} vs Input Power for {DUT}")