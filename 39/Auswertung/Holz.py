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

def drift_correction(time, B, degree=1):
    time = np.asarray(time)
    B = np.asarray(B)

    coeffs = np.polyfit(time, B, degree)
    drift = np.polyval(coeffs, time)

    B_corr = B - drift
    return B_corr, drift, coeffs


# ---------
# Data Path initialization
base_path = Path.cwd() / '39'
data_path = base_path / 'Auswertung' / 'Data'
img_path = base_path / 'Images'

# ---------
messreihe = Messreihe(data_path / 'Ringkern4_39.csv', N1=1010, N2=250, R=67.3, F=1.0)
DataHolz = messreihe.dataArray()

# shift correction
B_Shift = symmetric(DataHolz.iloc[:, 1], DataHolz.iloc[:,2], symPX=58)
DataH = DataHolz.iloc[:, 1] 
DataB = DataHolz.iloc[:,2] - B_Shift
print('Symmetrisierungsfaktor Holzkern: ' + str(B_Shift) + 'T')

plt1 = ScatterPlotter(xlabel='H [A/m]', ylabel='B [T]')
plt1.plot(DataH, DataB, grid=False, label='Messpunkte', xlim=False, ylim=False)
# plt1.save(img_path)
plt1.show()