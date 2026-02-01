import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset

x = np.linspace(0, 10, 1000)
y = np.sin(x) * np.exp(-0.1 * x)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x, y)
ax.set_title("Gesamtansicht mit Zoom-Inset")

# Inset erstellen
axins = inset_axes(ax, width="40%", height="40%", loc="upper right")

axins.plot(x, y)
axins.set_xlim(2, 4)
axins.set_ylim(-0.5, 0.5)

# Verbindung markieren
mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="0.5")

plt.show()
