import pandas as pd
from pathlib import Path

# Data Path initialization

# Determine script directory
base_path = Path(__file__).resolve().parent

# Paths for data and images
data_path = base_path / 'Data' / 'Datasheet.xlsx'
img_path = base_path.parent / 'Images'

# import data from path
Data = pd.read_excel(data_path, sheet_name='Planck', engine='openpyxl')