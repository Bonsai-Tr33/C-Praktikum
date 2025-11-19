# measuring the speed of propagation via standing waves

# dependencies
import numpy as np
import os
import pandas as pd
import statistics
from matplotlib import pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from pathlib import Path

# Method for calculating the speed of propagation
def SoP(f, l, Df=0):
    return f * l, l * Df

# method for frequency error calculation:
def Df (f, rel, count):
    return rel * f + count

# method for Damping calculation
def Damping(U, U0, DU=0, DU0=0):
    D = 20 * np.log10(U0 / U) #dB
    DD = 20 / np.log(10) * np.sqrt((DU0 / U0)**2 + (DU / U)**2)
    return D, DD

# calculating e_r
def e_r(c, v, Dv=0):
    return (c/v)**2 , 2* (c**2)/(v**3) * Dv

# Data Path initialization

# Determine script directory
base_path = Path(__file__).resolve().parent

# Paths for data and images
data_path = base_path / 'Data' / 'Datasheet.xlsx'
img_path = base_path.parent / 'Images'

# import data from path
Data = pd.read_excel(data_path, sheet_name='2122', engine='openpyxl')

WavelengthRatio = Data['Wavelength ratio'].tolist() # will be called WR further on
Frequency = Data['Frequency [Hz]'].tolist() # will be called f further on
Upp = Data['Voltage (U_PP) [V]'].tolist()
div = Data['div [V]'].tolist()

# seperating different WR
# initialising array via structure: WR = [[f0, Upp0, div0], [f1, Upp1, div1], ...]
WR4 = [] # WR for λ/4
WR34 = [] # WR for 3λ/4
WR2 = [] # WR for λ/2

# error of f measurement: user guide, page 159
DfRel = 51 * 10**(-6)
DfCount = 1

for i in range(len(WavelengthRatio)):
    if WavelengthRatio[i] == 'λ/4':
        WR4.append([Frequency[i], Df(Frequency[i], DfRel, DfCount),Upp[i], div[i]])
    elif WavelengthRatio[i] == '3λ/4':
        WR34.append([Frequency[i], Df(Frequency[i], DfRel, DfCount), Upp[i], div[i]])
    elif WavelengthRatio[i] == 'λ/2':
        WR2.append([Frequency[i], Df(Frequency[i], DfRel, DfCount), Upp[i], div[i]])
    else:
        print(f'WavelengthRatio Issue: {i}')

# Sanity check: (uncomment first argument in next line)
# print(WR4) #should print in position 0: [939991, 48.939541, 0.0136, 0.002]

# calculate wavelength from length of cable
l = 50
lam4 = 4*l
lam34 = 4/3 * l
lam2 = 2 * l

# calculating the medians and errors
f4 = statistics.median([x[0] for x in WR4])
Df4 = np.sqrt(sum([x[1] for x in WR4])) / len([x[1] for x in WR4])
f34 = statistics.median([x[0] for x in WR34])
Df34 = np.sqrt(sum([x[1] for x in WR34])) / len([x[1] for x in WR34])
f2 = statistics.median([x[0] for x in WR2])
Df2 = np.sqrt(sum([x[1] for x in WR2])) / len([x[1] for x in WR2])

# calculating speed of propagation for each frequency
SoP4 = SoP(f4, lam4, Df=Df4)
SoP34 = SoP(f34, lam34, Df=Df34)
SoP2 = SoP(f2, lam2, Df=Df2)

print(f'λ/4: f = {f4} ± {Df4} Hz')
print(f'3λ/4: f = {f34} ± {Df34} Hz')
print(f'λ/2: f = {f2} ± {Df2} Hz')

print('---------------------------------')

print(f'λ/4: SoP = {SoP4[0]} ± {SoP4[1]} m/s')
print(f'3λ/4: SoP = {SoP34[0]} ± {SoP34[1]} m/s')
print(f'λ/2: SoP = {SoP2[0]} ± {SoP2[1]} m/s')

print('---------------------------------')

# seperating Upp values for further analysis
Upp4 = []
Upp34 = []
Upp2 = []

for i in range(len(WavelengthRatio)):
    if WavelengthRatio[i] == 'λ/4':
        Upp4.append([Upp[i], 0.5 * div[i]])
    elif WavelengthRatio[i] == '3λ/4':
        Upp34.append([Upp[i], 0.5 * div[i]])
    elif WavelengthRatio[i] == 'λ/2':
        Upp2.append([Upp[i], 0.5 * div[i]])
    else:
        print(f'Upp Issue: {i}')

#print(Upp4)

# Calculate median voltage U and error DU for each wavelength ratio
U4 = statistics.median([x[0] for x in Upp4])
DU4 = np.sqrt(sum([x[1]**2 for x in Upp4])) / len(Upp4)
U34 = statistics.median([x[0] for x in Upp34])
DU34 = np.sqrt(sum([x[1]**2 for x in Upp34])) / len(Upp34)
U2 = statistics.median([x[0] for x in Upp2])
DU2 = np.sqrt(sum([x[1]**2 for x in Upp2])) / len(Upp2)

print(f'λ/4: U = {U4} ± {DU4} V')
print(f'3λ/4: U = {U34} ± {DU34} V')
print(f'λ/2: U = {U2} ± {DU2} V')

print('---------------------------------')

# initializing U0
U0 = 0.160
DU0 = 0.025

# calculating Damping D and error DD
D0, DD0 = Damping(U0, U0, DU0, DU0)
D4, DD4 = Damping(U4, U0, DU4, DU0)
D34, DD34 = Damping(U34, U0, DU34, DU0)
D2, DD2 = Damping(U2, U0, DU2, DU0)

# creating arrays and plotting damping
D = [D4, D2, D34]
DD = [DD4, DD2, DD34]

print(f'Damping(D, DD)= {D, DD}')

print('---------------------------------')

# plotting Damping over Frequency
plt.errorbar([f4, f2, f34], D,yerr=DD, capsize=5, label='Dämpfung in Abh. der Resonanzfrequenz', color='black', marker='x', linestyle='None') # plot with error bars

plt.xlabel(r'Frequenz $\omega$ [Hz]')
plt.ylabel('Dämpfung D [dB]')
plt.title('Dämpfung über Frequenz', loc='left')
plt.text(1, 1.05, 'Hannes Winkler und Moritz Langer, 12.11.2025', ha='right', va='top', transform=plt.gca().transAxes, fontsize=10)
plt.legend()

# locating and arranging ticks
plt.gca().yaxis.set_minor_locator(AutoMinorLocator(2))
plt.gca().xaxis.set_minor_locator(AutoMinorLocator(2))
plt.xticks(np.arange(800000, 3000100, 200000))
plt.yticks(np.arange(8, 30, 1))
plt.tick_params(axis='both', which='minor', direction='in', right=True, top=True)
plt.tick_params(axis='both', which='major', direction='in', right=True, top=True, length=5)

# limiting and setting plot layout
plt.ylim(13, 24)
plt.xlim(830000, 3000100)
plt.tight_layout()

# plot location
plt.savefig(img_path / 'DoverF.png')
# plt.show() # shows plot every run of the code, used for debugging

er4 = e_r(299792458, SoP4[0], SoP4[1])
er34 = e_r(299792458, SoP34[0], SoP34[1])
er2 = e_r(299792458, SoP2[0], SoP2[1])

print(f'er4 = {er4}')
print(f'er34 = {er34}')
print(f'er2 = {er2}')