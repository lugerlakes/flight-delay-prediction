import os
import pandas as pd

def load_raw_data(filename: str = "dataset_SCL.csv", data_dir: str = "data/raw") -> pd.DataFrame:
    """
    Load raw flight data from a CSV file.

    Parameters
    ----------
    filename : str
        Name of the CSV file.
    data_dir : str
        Relative path to the directory containing the file.

    Returns
    -------
    pd.DataFrame
        Loaded data as a pandas DataFrame.
    """
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    file_path = os.path.join(project_root, data_dir, filename)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found at: {file_path}")

    return pd.read_csv(file_path, low_memory=False)

