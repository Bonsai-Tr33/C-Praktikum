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

def HC(H, B, B_Tolerance=0.1):
    H = np.asarray(H)
    B = np.asarray(B)

    # select points close to B = 0
    mask = (np.abs(B) <= B_Tolerance) & (H<0)

    if np.sum(mask) < 2:
        raise ValueError("Zu wenige Punkte nahe B = 0. B_toleranz erhöhen!")

    H_0 = H[mask]

    # Median = Koerzitivfeldstärke
    H_C = np.mean(H_0)
    D_HC = np.std(H_0, ddof=1) / np.sqrt(len(H_0))

    return H_C, D_HC

# ---------
# Data Path initialization
base_path = Path.cwd() / '39'
data_path = base_path / 'Auswertung' / 'Data'
img_path = base_path / 'Images'

# ---------
# First measurements
messreihe1 = Messreihe(data_path / 'Ringspule1_39.csv', N1=605, N2=80, R=67.3, F=0.9)
Data1 = messreihe1.dataArray()

# shift correction
B_Shift = symmetric(Data1.iloc[:, 1], Data1.iloc[:,2], symPX=58)
DataH = Data1.iloc[:, 1] 
DataB = Data1.iloc[:,2] - B_Shift
print('Symmetrisierungsfaktor Ringkern 1: ' + str(B_Shift) + 'T')

# koerzitivfeldstärke measurement 1
HC1, DHC1 = HC(DataH, DataB)
print('Koerzitivfeldstärke Ringkern 1: (' + str(HC1) + ' ± ' + str(DHC1) + ') A/m')

plt1 = ScatterPlotter(xlabel='H [A/m]', ylabel='B [T]')
plt.scatter(HC1, 0, marker='x', color='red', label='H_C')
plt1.plot(DataH, DataB, grid=False, label='Messpunkte', xlim=True, xlimit=85, xstep=20, ylim=True, ylimit=1.2, ystep=0.2)
plt1.show()