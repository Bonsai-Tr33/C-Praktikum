# measuring the speed of light

# dependencies
import numpy as np
import os
import pandas as pd
import statistics
from matplotlib import pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from pathlib import Path

def c(x,t):
    return  2* (x-0.2315) / t

def dc(x, t, dx, dt):
    return np.sqrt((2/t*dx)**2+(2*(x-0.2315)/(t**2)*dt)**2)

Orte = [3.91, 4.02, 4.14, 7.92, 8.03, 8.15, 11.712, 11.822, 11.942]
Zeit = [24*10**(-9), 24*10**(-9), 28*10**(-9), 50*10**(-9), 52*10**(-9), 58*10**(-9), 78*10**(-9), 80*10**(-9), 86*10**(-9)]
dx = 0.0005
dt = 5*10**(-9)

Bip = []
for i in range(len(Orte)):
    Bip.append([c(Orte[i], Zeit[i]), dc(Orte[i], Zeit[i], dx, dt)])

SoL = sum([x[0] for x in Bip])/len(Bip)
DSoL = np.sqrt((1/(len(Bip)-1)* sum([(x[0]-SoL)**2 for x in Bip])))
print(SoL, DSoL)

'''
plt.errorbar(Zeit, Orte, xerr=dt, yerr=dx, marker='x', linestyle='None', label='Messpunkte mit Fehlerbalken', capsize=4)
plt.xlabel('Zeit t [s]')
plt.ylabel('Distanz l [m]')
plt.title('Lichtgeschwindigkeit', loc='left')
plt.text(1, 1.05, 'Hannes Winkler und Moritz Langer, 13.11.2025', ha='right', va='top', transform=plt.gca().transAxes, fontsize=10)
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
plt.show()
'''