import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from src.data.load_data import load_raw_data

df = load_raw_data()

print("Shape of dataframe:", df.shape)
print("Columns:", df.columns.tolist())
