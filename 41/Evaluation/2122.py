# measuring the speed of propagation via standing waves

# dependencies
import numpy as np
import os
import pandas as pd
import statistics

# Method for calculating speed of propagation
def SoP(f, l, Df=0):
    return f * l, l * Df

# method for frequency error calculation:
def Df (f, rel, count):
    return rel * f + count

# Get the path to the current script's directory
base_path = os.path.dirname(__file__)

# Build the data path relative to the script
data_path = os.path.join(base_path, 'Data', 'Datasheet.xlsx')

# import data from path
Data = pd.read_excel(data_path, sheet_name='2122', engine='openpyxl')

WavelengthRatio = Data['Wavelength ratio'].tolist() # will be called WR further on
Frequency = Data['Frequency [Hz]'].tolist() # will be called f further on
Upp = Data['Voltage (U_PP) [V]'].tolist()
div = Data['div [V]'].tolist()

print('Data Import succesfull!')

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

print('Error of Frequency is successfully calculated')
print('Data sorted by Wavelength Ratio.')

# Sanity check: (uncomment first argument in next line)
# print(WR4) #should print in position 0: [939991, 48.939541, 0.0136, 0.002]

# calculate wavelength from length of cable
l = 50
lam4 = l / 4
lam34 = 3* l / 4
lam2 = l / 2

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
Sop2 = SoP(f2, lam2, Df=Df2)

print('lam/4 f= ' + str(f4) + ' error: ' + str(Df4))
print('3lam/4 f= ' + str(f34) + ' error: ' + str(Df34))
print('lam/2 f= ' + str(f2) + ' error: ' + str(Df2))


'''
    Mittelwerte aus frequenz und Upp bilden. 
    Wie wird Fehler von Div mitgenommen? 
    Wie wird aus den aufgenommenen Daten Ausbreitungsgeschwindigkeit berechnet?
'''