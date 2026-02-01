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

def Br(H, B, H_Tolerance=0.5):
    H = np.asarray(H)
    B = np.asarray(B)

    # select points close to B = 0
    mask = (np.abs(H) <= H_Tolerance) & (B>0)

    if np.sum(mask) < 2:
        raise ValueError("Zu wenige Punkte nahe H = 0. H_toleranz erhöhen!")

    B_0 = B[mask]

    # Median = Koerzitivfeldstärke
    B_R = np.mean(B_0)
    D_BR = np.std(B_0, ddof=1) / np.sqrt(len(B_0))

    return B_R, D_BR

# ---------
# Data Path initialization
base_path = Path.cwd() / '39'
data_path = base_path / 'Auswertung' / 'Data'
img_path = base_path / 'Images'

# ---------
# First measurements
messreihe3 = Messreihe(data_path / 'Ringkern3Irre_39.csv', N1=1010, N2=53, R=67.3, F=1)
Data3 = messreihe3.dataArray()

# shift correction
B_Shift = symmetric(Data3.iloc[:, 1], Data3.iloc[:,2], symPX=58)
DataH = Data3.iloc[:, 1] 
DataB = Data3.iloc[:,2] - B_Shift
print('Symmetrisierungsfaktor Ringkern 1: ' + str(B_Shift) + 'T')

plt3 = ScatterPlotter(xlabel='H [A/m]', ylabel='B [T]')
plt3.plot(DataH, DataB, grid=False, label='Messpunkte', xlim=False, ylim=False)
# plt3.save(img_path)
plt3.show()