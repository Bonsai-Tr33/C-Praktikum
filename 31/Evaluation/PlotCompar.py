import numpy as np
from pathlib import Path
from scipy.optimize import brentq
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import pandas as pd

base_path = Path.cwd() / '31'
data_path = base_path / 'Evaluation' / 'Data' / 'Datasheet.xlsx'
img_path = base_path / 'Images'

# Parameter
a = 0.79*10**(-5)       # 10**5 Pa * m^6 / mol^2 
b = 86.7*10**(-6)       # m^3 / mol
T = 308.15              # K
# T = 35                # °C
R = 8.314               # Pa * m^3 / (K * mol)
n = 0.001319            # mol

Data35Tab = pd.read_excel(data_path, sheet_name='T = 35°C',engine='openpyxl') # 10^5 Pa, ml
Data35 = np.array([[x,y*10**(-6)] for x,y in zip(Data35Tab['Druck [10^5 Pa]'].tolist(), Data35Tab['Volumen [ml]'].tolist())]) # 10 ^5 Pa, m^3

def p_vdw(V):
    return (n*R*T)/(V - n*b) - (a*n**2)/(V**2)

# Plot
Vplot = np.linspace(0, 4*10**(-6), 100)

plt.plot(Vplot, p_vdw(Vplot), label='VdW', color='black')
plt.plot(Vplot, n*R*T/Vplot, label='ideales Gas', color='green', linestyle='--')
plt.plot(Data35[:,1], Data35[:,0], '8', label='T = 35 °C', color='orange', markersize=4)

# plt.tick_params(axis='both', which='minor', direction='in', right=True, top=True)
# plt.tick_params(axis='both', which='major', direction='in', right=True, top=True, length=5)
# plt.gca().yaxis.set_minor_locator(AutoMinorLocator(2))
# plt.gca().xaxis.set_minor_locator(AutoMinorLocator(2))

plt.xlabel('V')
plt.ylabel('p')
#plt.xlim(0,100)
#plt.ylim(-1, 5*10**6)
plt.legend()
plt.tight_layout()
plt.savefig(img_path / 'HA_VdW_Maxwell_COMP.png')
plt.show()