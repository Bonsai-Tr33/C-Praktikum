# measuring the propagation of speed (coaxial cable and delay cable)

# Dependencies
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

# Time difference (T_D) and length for the delay cable
T_D = 2.120 * 10**(-6)
DT_D = 50 * 10**(-9)

# calculating l_D and Dl_D from measurement series
L_D = [[0.480, 0.0005], [0.491, 0.0005], [0.487, 0.0005], [0.486, 0.0005], [0.490, 0.0005]]
l_D = sum([x[0] for x in L_D]) / len(L_D)
Dl_D = np.sqrt((1/(len(L_D)-1)) * sum([(x[0]-l_D)**2 for x in L_D]))

vProp_C = vProp(T_C, l_C, DT_C, Dl_C)
vProp_D = vProp(T_D, l_D, DT_D, Dl_D)

print(f't for coaxial cable: {T_C} s ± {DT_C} s')
print(f't for delay cable: {T_D} s ± {DT_D} s')


# print(f'Best value and error of the propagation speed of the coaxial cable in m/s: {vProp_C}')
# print(f'Best value and error of the propagation speed of the delay cable in m/s: {vProp_D}') # will remain 0 until length of delay cable is measured