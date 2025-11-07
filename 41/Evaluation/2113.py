# Dependencies
import matplotlib.pyplot as plt
import scipy.optimize
import math
import numpy as np

'''
    For Image reference:
        ALL0033
        ALL0037
'''


# Method for calculating best value and error
def vProp(T, l, DT=0, Dl=0):
    """
    Calculation according to Gaussian error
    
    return:
        v, Dv : tuple(float, float) — best values and error
    """
    v = (2 * l) / T
    Dv = np.sqrt((2/T * Dl)**2 + (2*l/(T**2) * DT)**2)
    return v, Dv

# Time difference (T_C) and length (l_C) for the coaxial cable
T_C = 520 * 10**(-9)
DT_C = 50 * 10**(-9)
l_C = 50
Dl_C = 0

# Time difference (T_D) and length (l_D = ?) for the delay cable
T_D = 2.120 * 10**(-6)
DT_D = 50 * 10**(-9)
l_D = 0
Dl_D = 0

vProp_C = vProp(T_C, l_C, DT_C, Dl_C)
vProp_D = vProp(T_D, l_D, DT_D, Dl_D)

print(f'Best value and error of the propagation speed of the coaxial cable in m/s: {vProp_C}')
print(f'Best value and error of the propagation speed of the delay cable in m/s: {vProp_D}') # will remain 0 until length of delay cable is measured