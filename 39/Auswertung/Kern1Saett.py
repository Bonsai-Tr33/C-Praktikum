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

# Seattigungsmessung
measure = Messreihe(data_path / 'Ringkern1Sätt_39.csv', N1=605, N2=80, R=67.3, F=0.9)
Data1 = measure.dataArray()

# shift correction
B_Shift = symmetric(Data1.iloc[:, 1], Data1.iloc[:,2], symPX=58)
DataH = Data1.iloc[:, 1] 
DataB = Data1.iloc[:,2] - B_Shift
print('Symmetrisierungsfaktor Ringkern 1: ' + str(B_Shift) + ' T')

# find saturation
satt1, Dsatt1 = saturation(DataH, DataB, 6, 7)
print('Satturation bei: (' + str(satt1) + ' ± ' + str(Dsatt1) + ') T, unbereinigt!!!!')
F = 0.9
satt1_cl, Dsatt1_cl = satt1/F , Dsatt1/F
print('bereinigte Satturation ist: (' + str(satt1_cl) + ' ± ' + str(Dsatt1_cl) + ') T')

plt1 = ScatterPlotter(xlabel='H [A/m]', ylabel='B [T]')
plt.hlines(satt1, -8, 8, label='satturiert')
plt1.plot(DataH, DataB, grid=False, label='Messpunkte', xlim=True, xlimit=7, xstep=1, ylim=False)
plt.legend(loc='center right')
plt1.show()