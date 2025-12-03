import numpy as np
from pathlib import Path
from scipy.optimize import brentq
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

base_path = Path.cwd() / '31'
img_path = base_path / 'Images'

# Parameter (Einheiten: bar, cm^3, K)
a = 3.658e6       # bar * cm^6 / mol^2
b = 42.75         # cm^3 / mol
T = 288.7         # K
R = 83.14         # bar * cm^3 / (K * mol)

def p_vdw(V):
    return R*T/(V - b) - a/(V**2)

def dpdV(V):
    return -R*T/(V - b)**2 + 2*a/(V**3)

# Spinodalen finden (Suche nach Vorzeichenwechseln von dpdV)
Vgrid = np.logspace(np.log10(b+1e-6), 5, 5000)
spin = []
for i in range(len(Vgrid)-1):
    if dpdV(Vgrid[i]) * dpdV(Vgrid[i+1]) < 0:
        try:
            root = brentq(dpdV, Vgrid[i], Vgrid[i+1])
            spin.append(root)
        except Exception:
            pass

spin = sorted(set(spin))
print("Spinodalen:", spin)

# Maxwell: Finde p0 so, dass integral_{V1}^{V2} (p(V)-p0) dV = 0 mit p(V1)=p(V2)=p0
V_left = spin[0]
V_right = spin[-1]
def area_for_p(pguess):
    # finde V1 in (b, V_left) und V2 in (V_right, large)
    V1 = brentq(lambda V: p_vdw(V)-pguess, b+1e-8, V_left-1e-8)
    V2 = brentq(lambda V: p_vdw(V)-pguess, V_right+1e-8, 1e6)
    Vs = np.linspace(V1, V2, 2000)
    area = np.trapz(p_vdw(Vs)-pguess, Vs)
    return area, V1, V2

p_low = p_vdw(V_right)
p_high = p_vdw(V_left)

# Rootfind p0 such that area_for_p(p0).area == 0
def f_for_root(p):
    area,_,_ = area_for_p(p)
    return area

p0 = brentq(f_for_root, p_low, p_high)
area, V1, V2 = area_for_p(p0)
print("p0 =", p0)
print("V1 =", V1, " V2 =", V2, " area =", area)

# Plot
Vplot = np.concatenate([np.linspace(b+1e-6, 500, 1000), np.linspace(500, 1e5, 1000)])
# plt.figure(figsize=(8,5))
plt.plot(Vplot, p_vdw(Vplot), label='VdW', color='black')
plt.plot(Vplot, R*T/Vplot, label='ideales Gas', color='green', linestyle='--')
plt.hlines(p0, V1, V2, colors='red', linestyles='dashed', label='Maxwell-Konstruktion')
# plt.scatter([V1,V2],[p0,p0])
plt.tick_params(axis='both', which='minor', direction='in', right=True, top=True)
plt.tick_params(axis='both', which='major', direction='in', right=True, top=True, length=5)
plt.gca().yaxis.set_minor_locator(AutoMinorLocator(2))
plt.gca().xaxis.set_minor_locator(AutoMinorLocator(2))

plt.xlabel('V (cm^3/mol)')
plt.ylabel('p (bar)')
plt.xlim(30,600)
plt.ylim(30, 200)
plt.legend()
plt.tight_layout()
plt.savefig(img_path / 'HA_VdW_Maxwell.png')
plt.show()

# print(base_path)