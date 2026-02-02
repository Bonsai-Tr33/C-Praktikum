from pathlib import Path
from importer import Messreihe
from scatterplt import ScatterPlotter
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

def linear_model(H, m, b):
    return m * H + b

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

# ---------
# Driftkorrektur (zeitabhängig!)
time = DataHolz.iloc[:, 0]
H_raw = DataHolz.iloc[:, 1]
B_raw = DataHolz.iloc[:, 2]

B_driftcorr, drift, coeffs = drift_correction(time, B_raw, degree=1)

print(f"Driftkoeffizienten (B(t)): {coeffs}")

# ---------
# Symmetrisierung NACH Driftkorrektur
B_Shift = symmetric(H_raw, B_driftcorr, symPX=58)

DataH = H_raw
DataB = B_driftcorr - B_Shift

print('Symmetrisierungsfaktor Holzkern: ' + str(B_Shift) + ' T')


popt, pcov = curve_fit(linear_model, DataH, DataB)
m_fit, b_fit = popt

sigma_m, sigma_b = np.sqrt(np.diag(pcov))

print(f"Best-Fit Steigung m = {m_fit:.3e} ± {sigma_m:.3e}")

H_plot = np.linspace(-200, 200, 500)

B_best = linear_model(H_plot, m_fit, b_fit)

plt1 = ScatterPlotter(xlabel='H [A/m]', ylabel='B [T]')
plt1.plot(DataH, DataB, grid=False, label='Messpunkte', xlim=True, xlimit=150, xstep=25, ylim=False)
plt.plot(H_plot, B_best, color='red', label='Linearer Fit')
plt.legend()
plt1.show()

nu = m_fit / (1.256637*10**(-6))
Dnu = sigma_m / (1.256637*10**(-6))
print('permeabilität: (' + str(nu) + ' ± ' + str(Dnu) + ')')