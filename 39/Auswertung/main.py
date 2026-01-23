from pathlib import Path
from importer import Messreihe
from scatterplt import ScatterPlotter
import matplotlib.pyplot as plt
import numpy as np

def symmetric(dataX, dataY, symPX=1000):
    dataX = np.asarray(dataX)
    dataY = np.asarray(dataY)

    # find indizes
    idx_pos = np.argmin(np.abs(dataX - symPX))
    idx_neg = np.argmin(np.abs(dataX + symPX))

    Bmax = dataY[idx_pos]
    Bmin = dataY[idx_neg]

    B_shift = Bmax - (Bmax - Bmin) / 2

    return B_shift

# ---------
# Data Path initialization
base_path = Path.cwd() / '39'
data_path = base_path / 'Auswertung' / 'Data'
img_path = base_path / 'Images'

# ---------
# First measurements
messreihe1 = Messreihe(data_path / 'Ringspule1_39.csv', N1=605, N2=80, R=67.3, F=0.9)
Data1 = messreihe1.dataArray()

result = messreihe1.hysteresis_drift_from_arrays(
    Data1.iloc[:, 0],
    Data1.iloc[:, 1],
    Data1.iloc[:, 2]
)

print("Drift:", result["drift"])
print("Δt:", result["delta_t"])

# shift correction
B_Shift = symmetric(Data1.iloc[:, 1], Data1.iloc[:,2], symPX=58)
DataH = Data1.iloc[:, 1] 
DataB = Data1.iloc[:,2] - B_Shift

'''
plt1 = ScatterPlotter(xlabel='H [A/m]', ylabel='B [T]')
plt1.plot(DataH, DataB, grid=False, label='Messpunkte', xlim=True, xlimit=85, xstep=20, ylim=True, ylimit=1.2, ystep=0.2)
plt1.show()
'''