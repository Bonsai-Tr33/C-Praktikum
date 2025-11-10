# measuring the speed of propagation via standing waves

# dependencies
import numpy as np
import os
import pandas as pd

# Method for calculating speed of propagation
def SoP(f, l, Df):
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

for i in range(len(WavelengthRatio)):
    if WavelengthRatio[i] == 'λ/4':
        WR4.append([Frequency[i], Upp[i], div[i]])
    elif WavelengthRatio[i] == '3λ/4':
        WR34.append([Frequency[i], Upp[i], div[i]])
    elif WavelengthRatio[i] == 'λ/2':
        WR2.append([Frequency[i], Upp[i], div[i]])
    else:
        print(f'WavelengthRatio Issue: {i}')

print('Data sorted by Wavelength Ratio.')

# calculate wavelength from length of cable
l = 50
lam4 = l / 4
lam34 = 3* l / 4
lam2 = l / 2

# error of f measurement: user guide, page 159
DfRel = 51 * 10**(-6)
DfCount = 1



'''
    Mittelwerte aus frequenz und Upp bilden. 
    Wie wird Fehler von Div mitgenommen? 
    Wie wird aus den aufgenommenen Daten Ausbreitungsgeschwindigkeit berechnet?
'''