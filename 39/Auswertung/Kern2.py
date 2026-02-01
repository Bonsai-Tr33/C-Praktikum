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

def saturation(H, B, xmin, xmax):
    mask = (H >= xmin) & (H<=xmax)
    if np.sum(mask) < 5:
        raise ValueError("Zu wenige Punkte innerhalb des gewählten Bereichs")

    satArr = B[mask]
    return np.mean(satArr), np.std(satArr, ddof=1) / np.sqrt(len(satArr))


# ---------
# Data Path initialization
base_path = Path.cwd() / '39'
data_path = base_path / 'Auswertung' / 'Data'
img_path = base_path / 'Images'

# ---------
# First measurements
messreihe2 = Messreihe(data_path / 'Ringkern2_39.csv', N1=605, N2=56, R=67.3, F=0.9)
Data2 = messreihe2.dataArray()

# shift correction
B_Shift = symmetric(Data2.iloc[:, 1], Data2.iloc[:,2], symPX=58)
DataH = Data2.iloc[:, 1] 
DataB = Data2.iloc[:,2] - B_Shift
print('Symmetrisierungsfaktor Ringkern 1: ' + str(B_Shift) + 'T')

# koerzitivfeldstärke measurement 1
HC2, DHC2 = HC(DataH, DataB, B_Tolerance=1)
print('Koerzitivfeldstärke Ringkern 1: (' + str(HC2) + ' ± ' + str(DHC2) + ') A/m')

# remanenz measurement 1
BR2, DBR2 = Br(DataH, DataB)
print('Remanenz Ringkern 1: (' + str(BR2) + ' ± ' + str(DBR2) + ') T')

# find saturation
satt1, Dsatt1 = saturation(DataH, DataB, 35, 50)
print('Satturation bei: (' + str(satt1) + ' ± ' + str(Dsatt1) + ') T, unbereinigt!!!!')
F = 0.9
satt1_cl, Dsatt1_cl = satt1/F , Dsatt1/F
print('bereinigte Satturation ist: (' + str(satt1_cl) + ' ± ' + str(Dsatt1_cl) + ') T')


plt2 = ScatterPlotter(xlabel='H [A/m]', ylabel='B [T]')
plt.scatter(HC2, 0, marker='x', color='red', label='H_C', zorder=5)
plt.scatter(0, BR2, marker='x', color='orange', label='B_r', zorder=5)
plt.hlines(satt1, -50, 50, label='satturiert')
plt2.plot(DataH, DataB, grid=False, label='Messpunkte', xlim=True, xlimit=50, ylim=False)
plt.legend(loc='lower right')
plt2.save(img_path / 'Hyster2.png')
plt2.show()