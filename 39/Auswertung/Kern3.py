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

def drift_correction(time, B, degree=1):
    time = np.asarray(time)
    B = np.asarray(B)

    coeffs = np.polyfit(time, B, degree)
    drift = np.polyval(coeffs, time)

    B_corr = B - drift
    return B_corr, drift, coeffs

def hysteresis_area(H, B):
    H = np.asarray(H)
    B = np.asarray(B)

    # numerisches Linienintegral
    area = np.trapz(B, H)

    return abs(area)

# ---------
# Data Path initialization
base_path = Path.cwd() / '39'
data_path = base_path / 'Auswertung' / 'Data'
img_path = base_path / 'Images'

# ---------
# third measurements
messreihe3 = Messreihe(data_path / 'Ringkern3_2_39.csv', N1=1010, N2=53, R=67.3, F=1)
Data3 = messreihe3.dataArray()

# Driftkorrektur (zeitabhängig!)
time = Data3.iloc[:, 0]
H_raw = Data3.iloc[:, 1]
B_raw = Data3.iloc[:, 2]

B_driftcorr, drift, coeffs = drift_correction(time, B_raw, degree=1)

print(f"Driftkoeffizienten (B(t)): {coeffs}")

# shift correction
B_Shift = symmetric(H_raw, B_driftcorr, symPX=58)
DataH = H_raw 
DataB = B_driftcorr + B_Shift
print('Symmetrisierungsfaktor Ringkern 3: ' + str(B_Shift) + 'T')

# koerzitivfeldstärke measurement 3
HC3, DHC3 = HC(DataH, DataB, B_Tolerance=0.001)
print('Koerzitivfeldstärke Ringkern 3: (' + str(HC3) + ' ± ' + str(DHC3) + ') A/m')

# remanenz measurement 3
BR3, DBR3 = Br(DataH, DataB)
print('Remanenz Ringkern 3: (' + str(BR3) + ' ± ' + str(DBR3) + ') T')

plt1 = ScatterPlotter(xlabel='H [A/m]', ylabel='B [T]')
plt.scatter(HC3, 0, marker='x', color='red', label='H_C', zorder=5)
plt.scatter(0, BR3, marker='x', color='orange', label='B_r', zorder=5)
plt1.plot(DataH, DataB, grid=False, label='Messpunkte', xlim=False, ylim=False)
# plt1.save(img_path)
plt1.show()

# numeric integral
A = hysteresis_area(DataH, DataB)
print('Flächeninhalt der Hysteresekurve: ' + str(A))
print('Ummagnetisierungsverluste: ' + str(A/(8.25*10**3)) + ' J/kg')