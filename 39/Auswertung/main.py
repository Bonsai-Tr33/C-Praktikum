from pathlib import Path
from importer import Messreihe
from scatterplt import ScatterPlotter
import matplotlib.pyplot as plt

# ---------
# Data Path initialization
base_path = Path.cwd() / '39'
data_path = base_path / 'Auswertung' / 'Data'
img_path = base_path / 'Images'

# ---------
# First measurements
messreihe1 = Messreihe(data_path / 'Ringspule1_39.csv', N1=605, N2=80)
Data1 = messreihe1.dataArray()
plt1 = ScatterPlotter(xlabel='H [A/m]', ylabel='B [T]')
plt1.plot(Data1.iloc[:, 0], Data1.iloc[:, 1], grid=True)
plt1.show()
plt1.save(img_path)
