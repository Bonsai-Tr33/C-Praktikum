from pathlib import Path
from importer import Messreihe
from scatterplt import ScatterPlotter
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset
from matplotlib.ticker import AutoMinorLocator


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
messreihe3 = Messreihe(data_path / 'Ringkern3entmag_39.csv', N1=1010, N2=53, R=67.3, F=1)
Data3 = messreihe3.dataArray()

# shift correction
B_Shift = symmetric(Data3.iloc[:, 1], Data3.iloc[:,2], symPX=58)
DataH = Data3.iloc[:, 1] 
DataB = Data3.iloc[:,2] - B_Shift
print('Symmetrisierungsfaktor Ringkern 1: ' + str(B_Shift) + 'T')


fig, plt3 = plt.subplots(figsize=(8,5))
plt3.scatter(DataH, DataB, label='Messpunkte', c='black', s=0.5, zorder=4)
plt3.axvline(x=0, color='grey', linestyle='--', zorder=1, alpha=0.5)
plt3.axhline(y=0, color='grey', linestyle='--', zorder=1, alpha=0.5)
plt3.set_xlabel('H [A/m]')
plt3.set_ylabel(ylabel='B [T]')
plt3.tick_params(axis='both', which='minor', direction='in', right=True, top=True)
plt3.tick_params(axis='both', which='major', direction='in', right=True, top=True, length=5)
plt3.legend()

plt3in = inset_axes(plt3, width='40%', height='40%', loc='lower right',bbox_to_anchor=(0, 0.08, 1, 1), bbox_transform=plt3.transAxes)
plt3in.scatter(DataH, DataB, c='black', marker='.', s=1)
plt3in.set_xlim(-2,2)
plt3in.set_ylim(-0.5, 0.5)
mark_inset(plt3, plt3in, loc1=1, loc2=2, lw=1)
plt.savefig(img_path / 'Hyster3_entmag.png')
plt.show()