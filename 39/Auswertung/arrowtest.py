import matplotlib.pyplot as plt
import numpy as np

H = np.array([-2, -1, 0, 1, 2, 1, 0, -1, -2])
B = np.array([-1, -0.5, 0, 0.8, 1, 0.6, 0, -0.6, -1])

plt.plot(H, B, 'k')

plt.annotate(
    '',
    xy=(0.8, 0.9),      # Pfeilspitze
    xytext=(0.2, 0.6),  # Pfeilanfang
    arrowprops=dict(
        arrowstyle='->',
        color='red',
        lw=2
    )
)


plt.xlabel('H')
plt.ylabel('B')
plt.show()
