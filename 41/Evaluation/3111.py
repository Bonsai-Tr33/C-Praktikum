# measuring the speed of light

# dependencies
import numpy as np
import os
import pandas as pd
import statistics
from matplotlib import pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from pathlib import Path
import scipy.optimize as opt

# Data Path initialization

# Determine script directory
base_path = Path(__file__).resolve().parent

# Paths for data and images
data_path = base_path / 'Data' / 'Datasheet.xlsx'
img_path = base_path.parent / 'Images'

def c(x,t):
    return  2* (x-0.2315) / t

def dc(x, t, dx, dt):
    return np.sqrt((2/t*dx)**2+(2*(x-0.2315)/(t**2)*dt)**2)

def lin(x, m, b):
    return m*x + b

Orte = [3.91, 4.02, 4.14, 7.92, 8.03, 8.15, 11.712, 11.822, 11.942]
Zeit = [24*10**(-9), 24*10**(-9), 28*10**(-9), 50*10**(-9), 52*10**(-9), 58*10**(-9), 78*10**(-9), 80*10**(-9), 86*10**(-9)]
dx = 0.001
dt = 5*10**(-9)

Bip = []
for i in range(len(Orte)):
    Bip.append([c(Orte[i], Zeit[i]), dc(Orte[i], Zeit[i], dx, dt)])

SoL = sum([x[0] for x in Bip])/len(Bip)
DSoL = np.sqrt((1/(len(Bip)-1)* sum([(x[0]-SoL)**2 for x in Bip])))
print(SoL, DSoL)

param, cov = opt.curve_fit(lin, Zeit, Orte, sigma=[dt]*len(Zeit), absolute_sigma=True)
m = param[0]
dm = np.sqrt(cov[0][0])
b = param[1]
db = np.sqrt(cov[1][1])

xval = np.linspace(0, 10*10**(-8), 100)

plt.errorbar(Zeit, Orte, xerr=dt, yerr=dx, marker='x', linestyle='None', label='Messpunkte mit Fehlerbalken', capsize=4)
plt.plot(xval, lin(xval, m, b), label='Lineare Ausgleichsrechnung', color='red')
plt.xlabel('Zeit t [s]')
plt.ylabel('Distanz l [m]')
plt.title('Lichtgeschwindigkeit', loc='left')
# plt.text(1, 1.05, 'Hannes Winkler und Moritz Langer, 13.11.2025', ha='right', va='top', transform=plt.gca().transAxes, fontsize=10)
plt.legend()


# locating and arranging ticks
plt.gca().yaxis.set_minor_locator(AutoMinorLocator(2))
plt.gca().xaxis.set_minor_locator(AutoMinorLocator(2))
#plt.xticks(np.arange(800000, 3000100, 200000))
#plt.yticks(np.arange(8, 30, 1))
plt.tick_params(axis='both', which='minor', direction='in', right=True, top=True)
plt.tick_params(axis='both', which='major', direction='in', right=True, top=True, length=5)

# limiting and setting plot layout
plt.xlim(0, 10*10**(-8))
plt.ylim(2, 14)
plt.tight_layout()
plt.savefig(img_path / 'SOPLight.png')
# plt.show()
