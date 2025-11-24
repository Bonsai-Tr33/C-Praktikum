import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import AutoMinorLocator
import scipy.optimize as opt

def lin(x, a, b):
    return a*x+b

e = 1.602176634 * 10**(-19)  # elementary charge in C

# Data Path initialization

# Determine script directory
base_path = Path(__file__).resolve().parent

# Paths for data and images
data_path = base_path / 'Data' / 'Datasheet.xlsx'
img_path = base_path.parent / 'Images'

# import data from path
Data = pd.read_excel(data_path, sheet_name='Planck', engine='openpyxl')

U366 = [[-x, y] for x, y in zip(Data['U (366nm)'].tolist(), Data['Error U (366nm)'].tolist())]
I366 = [[x, y] for x, y in zip(Data['I (366nm)'].tolist(), Data['Error I (366nm)'].tolist())]

U436 = [[-x,y] for x,y in zip(Data['U (436nm)'].tolist(), Data['Error U (436nm)'].tolist())]
I436 = [[x, y] for x, y in zip(Data['I (436nm)'].tolist(), Data['Error I (436nm)'].tolist())]

U546 = [[-x, y] for x, y in zip(Data['U (546nm)'].tolist(), Data['Error U (546nm)'].tolist())]
I546 = [[x, y] for x, y in zip(Data['I (546nm)'].tolist(), Data['Error I (546nm)'].tolist())]

U578 = [[-x, y] for x, y in zip(Data['U (578nm)'].tolist(), Data['Error U (578nm)'].tolist())]
I578 = [[x,y] for x,y in zip(Data['I (578nm)'].tolist(), Data['Error I (578nm)'].tolist())]

U405 = np.array([[-x, y] for x, y in zip(Data['U (405nm)'].tolist(), Data['Error U (405nm)'].tolist())])
U405 = U405[~np.isnan(U405).all(axis=1)]
I405 = np.array([[x,y] for x,y in zip(Data['I (405nm)'].tolist(), Data['Error I (405nm)'].tolist())])
I405 = I405[~np.isnan(I405).all(axis=1)]

# setting fit range 
# keep only points with U in (-inf, -1.2]
maskH = U405[:, 0] <= -1.48
U405H = U405[maskH]
I405H = I405[maskH]

maskV = U405[:, 0] >= -0.5
U405V = U405[maskV]
I405V = I405[maskV]

params405H, cov405H = opt.curve_fit(lin, [x[0] for x in U405H], [x[0] for x in I405H], sigma=[x[1] for x in I405H], absolute_sigma=True)
errors405H = np.sqrt(np.diag(cov405H))
print(f'Fit parameters for 405nm (horizontal): a = {params405H[0]} ± {errors405H[0]}, b = {params405H[1]} ± {errors405H[1]}')

paraams405V, cov405V = opt.curve_fit(lin, [x[0] for x in U405V], [x[0] for x in I405V], sigma=[x[1] for x in I405V], absolute_sigma=True)
errors405V = np.sqrt(np.diag(cov405V))
print(f'Fit parameters for 405nm (vertical): a = {paraams405V[0]} ± {errors405V[0]}, b = {paraams405V[1]} ± {errors405V[1]}')

fit_range = np.linspace(-5, 5, 100)

# plotting
plt.errorbar([x[0] for x in U405], [x[0] for x in I405],xerr=[x[1] for x in U405], yerr=[x[1] for x in I405], capsize=5, label='PLOT', color='black', marker='x', linestyle='None') # plot with error bars
plt.plot(fit_range, lin(fit_range, params405H[0], params405H[1]), label='Fit Horizontalteil', color='red') # plot fit line
plt.plot(fit_range, lin(fit_range, paraams405V[0], paraams405V[1]), label='Fit Vertikalteil', color='blue', linestyle='--') # plot fit line

plt.xlabel('U')
plt.ylabel('I')
plt.title('Titel', loc='left')
plt.text(1, 1.05, 'Hannes Winkler und Moritz Langer, 24.11.2025', ha='right', va='top', transform=plt.gca().transAxes, fontsize=10)
plt.legend()

# locating and arranging ticks
plt.gca().yaxis.set_minor_locator(AutoMinorLocator(2))
plt.gca().xaxis.set_minor_locator(AutoMinorLocator(2))
# plt.xticks(np.arange(800000, 3000100, 200000))
# plt.yticks(np.arange(8, 30, 1))
plt.tick_params(axis='both', which='minor', direction='in', right=True, top=True)
plt.tick_params(axis='both', which='major', direction='in', right=True, top=True, length=5)

# limiting and setting plot layout
plt.ylim(-0.5, 1.7)
plt.xlim(-3, 0.1)
# plt.tight_layout()

# plot location
plt.savefig(img_path / 'Planck405.png')
plt.show() # shows plot every run of the code, used for debugging
