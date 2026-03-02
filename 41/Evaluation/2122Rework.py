import numpy as np
import pandas as pd
import statistics
import matplotlib.pyplot as plt
from pathlib import Path
from matplotlib.ticker import AutoMinorLocator

# =========================
# Konstanten & Parameter
# =========================
C0 = 299_792_458          # Lichtgeschwindigkeit [m/s]
L_CABLE = 50              # Kabellänge [m]

# =========================
# Hilfsfunktionen
# =========================
def median_and_error(values):
    """
    Median und statistischer Fehler des Medians
    """
    med = statistics.median(values)
    err = np.sqrt(
        sum((x - med)**2 for x in values) /
        (len(values) * (len(values) - 1))
    )
    return med, err


def damping_db(U, U_ref):
    """
    Dämpfung in dB (Spannungsverhältnis)
    """
    return 20 * np.log10(U_ref / U)


# =========================
# Daten laden
# =========================
base_path = Path(__file__).resolve().parent
data_path = base_path / 'Data' / 'Datasheet.xlsx'
img_path = base_path.parent / 'Images'
data = pd.read_excel(data_path, sheet_name='2122')

# Gruppierung nach Wellenlänge
groups = {
    'λ/4': [],
    'λ/2': [],
    '3λ/4': []
}

for _, row in data.iterrows():
    groups[row['Wavelength ratio']].append(row)

# =========================
# Auswertung
# =========================
results = []

for key, rows in groups.items():
    freqs = [r['Frequency [Hz]'] for r in rows]
    volts = [r['Voltage (U_PP) [V]'] for r in rows]

    f_med, f_err = median_and_error(freqs)
    U_med, _ = median_and_error(volts)

    # Aus Resonanzbedingung: v = f * λ
    if key == 'λ/4':
        lam = 4 * L_CABLE
    elif key == 'λ/2':
        lam = 2 * L_CABLE
    else:
        lam = 4/3 * L_CABLE

    v = f_med * lam

    results.append({
        'freq_MHz': f_med / 1e6,
        'U': U_med,
        'v': v
    })

# =========================
# Referenzspannung (kleinste Frequenz)
# =========================
# U_ref = min(r['U'] for r in results)
U_ref = max(r['U'] for r in results)

for r in results:
    r['D_dB'] = damping_db(r['U'], U_ref)
    r['D_dB_per_m'] = r['D_dB'] / L_CABLE   # <<< WICHTIG!

# =========================
# Fehler der Dämpfung
# =========================
for r in results:
    DU = 0.5 * np.mean(data['div [V]'])  # konservative Abschätzung
    r['DD_dB'] = (20 / np.log(10)) * (DU / r['U'])
    r['DD_dB_per_m'] = r['DD_dB'] / L_CABLE

for r in results:
    print(
        f"f = {r['freq_MHz']:.2f} MHz: "
        f"D = {r['D_dB_per_m']:.4f} ± {r['DD_dB_per_m']:.4f} dB/m"
    )


# =========================
# Plot
# =========================
freqs = [r['freq_MHz'] for r in results]
damps = [r['D_dB_per_m'] for r in results]
damp_err = np.array([r['DD_dB_per_m'] for r in results])

plt.errorbar(
    freqs,
    damps,
    yerr=damp_err,
    fmt='x',
    color='black',
    capsize=4,
    label='Messwerte'
)

plt.xlabel(r'Frequenz $\omega$ [MHz]')
plt.ylabel('Dämpfung D [dB/m]')
plt.title('Dämpfung über Frequenz', loc='left')
plt.legend()

# locating and arranging ticks
plt.gca().yaxis.set_minor_locator(AutoMinorLocator(2))
plt.gca().xaxis.set_minor_locator(AutoMinorLocator(2))
plt.xticks(np.arange(0,3.5,0.5))
#plt.yticks(np.arange(-0.14, 0.04, 0.02))
plt.tick_params(axis='both', which='minor', direction='in', right=True, top=True)
plt.tick_params(axis='both', which='major', direction='in', right=True, top=True, length=5)

# limiting and setting plot layout
plt.ylim(-0.02, 0.15)
plt.xlim(0.7, 3)
plt.tight_layout()
plt.savefig(img_path / 'DoverF.png')
# plt.tight_layout()
plt.show()