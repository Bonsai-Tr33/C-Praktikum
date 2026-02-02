import pandas as pd 

import matplotlib.pyplot as plt

import math

import numpy as np

from scipy import odr


filename=r"/Users/Moritz/Documents/GitHub/C-Praktikum/39/Auswertung/AuswertungTim/Capstone Data Holz.txt.tsv"

def sci(x):
    # ersetzt Komma durch Punkt, damit float() und wissenschaftliche Notation funktioniert
    return float(x.replace(",", "."))

df = pd.read_csv(filename,
sep=r"\s+",     # Spalten durch beliebige Leerzeichen getrennt
skiprows=1,     # erste Überschriftenzeile überspringen
names=["t", "Uind", "UR"],
converters={"t": sci, "Uind": sci, "UR": sci}
)


"""
print(df.info())
print(df.head())
plt.scatter(
    x=df["UR"], y=df["Uind"],
    color="blue", s=2)
plt.xlabel("UR")
plt.ylabel("Uind")
plt.show()
"""

Uind_err = 0.001
Ur_err = 0.001


#####################################################################################################################
#   Drift bereinigen 
#       Drift = (UindEnde-UindAnf)/(tEnde-tAnf)
#       Uindbereinigt = Uind + Drift*t
lastindex = df.shape[0] - 1
dUind = df.loc[lastindex,"Uind"]-df.loc[0,"Uind"]
dt = df.loc[lastindex,"t"]-df.loc[0,"t"]
drift = dUind/dt
drift_err = math.sqrt( (Uind_err/(dt))**2 + (-Uind_err/(dt))**2 )
print(f"dUind: {dUind} dt: {dt} drift: {drift} drifterr: {drift_err}")
df["Uindber"] = df["Uind"] - drift * df["t"]
df["Uindber_err"] = np.sqrt( Uind_err**2 + (df["t"]*drift_err)**2 )


#####################################################################################################################
#   Symmetrisieren
#       Bverschieb = Bmax - (Bmax-Bmin)/2
#       Bsym = B - Bverschieb
max = df["Uindber"].max()
min = df["Uindber"].min()
Verschiebung = (max + min)/2
max_err = df.loc[df["Uindber"] == df["Uindber"].max(), "Uindber_err"].values[0]
min_err = df.loc[df["Uindber"] == df["Uindber"].min(), "Uindber_err"].values[0]
print(f"Verschiebung: {Verschiebung}")
df["Uindsym"] = df["Uindber"] - Verschiebung
df["Uindsym_err"] = np.sqrt( df["Uindber_err"]**2 + (max_err/2)**2 + (min_err/2)**2 )


#####################################################################################################################
#   Calculate H
N1 = 1010 # Windungen der felderzeugenden Spule
da = 260e-3 # Außendurchmesser in m
di = 220e-3 # Innendurchmesser in m
d = (da + di)/2 # Mittlerer Kreisdurchmesser des ringförmigen M aterialkerns in m
R = 67.3 # Widerstand über welchen die Spannung abgenommen wurde
R_err = R*0.01 + 1.0
print(f"Durchmesser: {d}")
df["H"] = (N1 / (math.pi*d*R)) *df["UR"]
df["H_err"] = np.sqrt( (R_err*df["UR"]*N1/(math.pi*d*(R**2)))**2 + (Ur_err*N1 / (math.pi*d*R))**2 )


#####################################################################################################################
#   Calculate B
k = 5e-3 # Umrechnungsfaktor von Integral(Uind) zu Ausgangspannung U in Vs/V
N2 = 250 # Windungen der zu induzierenden Spule
Füllfaktor = 1 # Wie viel from Kern ist wirklich dieses Material
h = 30e-3 
A = h * (da-di)/2 * Füllfaktor
df["B"] = (k / (N2 * A)) * df["Uindsym"]
df["B_err"] = df["Uindsym_err"] * k/(N2*A)

df["B"] = df["B"] * 1000 # von T in mT umgerechnet
df["B_err"] = df["B_err"] * 1000




#####################################################################################################################
#   Ausgleichsgerade berechnen
#weights = 1 / df["B_err"].values #Das beachtet nur die y-Fehler
weights = 1 / (df["B_err"].values+df["H_err"].values)
coeffs, cov = np.polyfit(df["H"].values, df["B"].values, 1, w=weights, cov=True)
m, b = coeffs
m_err = np.sqrt(cov[0,0])
b_err = np.sqrt(cov[1,1])

print(f"Steigung m = {m:.6e} ± {m_err:.6e}")
print(f"Achsenabschnitt b = {b:.6e} ± {b_err:.6e}")


"""
# Lineares Modell
def linear_model(B, H):
    m, b = B
    return m*H + b

# Startwerte
beta0 = np.polyfit(df["H"], df["B"], 1)

# RealData mit H- und B-Fehlern
data = odr.RealData(df["H"].values, df["B"].values,
                    sx=df["H_err"].values, sy=df["B_err"].values)

# ODR ausführen
model = odr.Model(linear_model)
odr_fit = odr.ODR(data, model, beta0=beta0)
odr_fit.set_job(fit_type=0)
out = odr_fit.run()
out.pprint()  # hier siehst du m ± m_err, b ± b_err

# Ergebnisse
m, b = out.beta
m_err, b_err = out.sd_beta
print(f"Steigung m = {m:.6e} ± {m_err:.6e}")
print(f"Achsenabschnitt b = {b:.6e} ± {b_err:.6e}")
"""


"""
coeffs = np.polyfit(df["H"], df["B"], 1, cov=True)
m, b = coeffs[0]          # Steigung, Achsenabschnitt
cov = coeffs[1]           # Kovarianzmatrix
m_err = np.sqrt(cov[0,0]) # Fehler von m
b_err = np.sqrt(cov[1,1]) # Fehler von b

print(f"Steigung m = {m:.6e} ± {m_err:.6e}")
print(f"Achsenabschnitt b = {b:.6e} ± {b_err:.6e}")
"""

# Fitlinie erzeugen
x_fit = np.linspace(-200, 200, 500)
y_fit = m * x_fit + b






#####################################################################################################################
#   Relative Permeabilität berechnen

# m stammt aus B in mT, also zuerst in T umrechnen
m_T = m * 1e-3      # m in T/A/m
m_err_T = m_err * 1e-3
mu0 = 4*math.pi*1e-7
mur = m_T / mu0
mur_err = m_err_T / mu0

print(f"Relative Permeabilität mu_r = {mur:.6e} ± {mur_err:.6e}")



plt.scatter( x=df["H"], y=df["B"], color="blue", s=2, label="")
"""
plt.errorbar(
    df["H"], df["B"], 
    xerr=df["H_err"], yerr=df["B_err"], 
    fmt='o', color='blue', ecolor='lightgray', elinewidth=1, capsize=2, markersize=3, label="Messwerte"
)"""
plt.plot(x_fit, y_fit, color="red", label="Regressionsgerade")

# Min- und Max-Geraden
y_fit_max = (m+m_err) * x_fit + (b-b_err)
y_fit_min = (m-m_err) * x_fit + (b+b_err)

plt.plot(x_fit, y_fit_max, color="red", linestyle="--", linewidth=0.5, label="Min- und Max-Gerade")
plt.plot(x_fit, y_fit_min, color="red", linestyle="--", linewidth=0.5)

# Normale Zahlen an den Achsen (keine e-6 Notation)
plt.ticklabel_format(style='plain')

plt.xlim(-170,170)
plt.ylim(-0.50,0.50)

# Achsenbeschriftungen
plt.xlabel("Magnetfeldstärke H [A/m]")
plt.ylabel("Magnetische Flussdichte B [mT]")

# Ticks nach innen auf allen vier Seiten
plt.tick_params(direction='in', top=True, right=True)

# Gitter einschalten
plt.grid(True)

plt.legend(loc="upper left")

plt.show()

print(df)



plt.scatter( x=df["B"], y=df["B_err"], color="blue", s=2, label="")
plt.show()
plt.scatter( x=df["H"], y=df["H_err"], color="blue", s=2, label="")
plt.show()