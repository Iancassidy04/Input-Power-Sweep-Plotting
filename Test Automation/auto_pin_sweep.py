# Ian Cassidy
# Harmonic Transponder
# Sept 24 2026

''' Automatic Input Power Sweep of Agilent E4422B ESG signal generator and peak search on Agilent N9010A EXA signal analyzer
    For input frequency f0 and its harmonics.'''

import numpy as np

# Sweep Parameters
F = 525e6           # Desired fundamental Frequency
P_low = -30         # Starting input power in dbm
P_high = 10         # Final input power in dbm
P_step = 0.5        # Input power step size

# Analyzer Parameters
M = 4                   # Number of modes of interest
BW = 1e3                # Resolution bandwidth
SPAN = 10e3             # Frequency span around center frequency F

# Connect to signal generator
P_steps = (P_high - P_low) / P_step
P_in = np.linspace(P_low, P_high, P_steps)


for i in range(1, M, 1):
    '''
    Set read parameters for SA
    Freq = M * F

    '''

    for i in range(P_in):
        '''
        Set output parameters for SG

        '''

        ''' 
        Save tuple of P_in and read peak val

        '''