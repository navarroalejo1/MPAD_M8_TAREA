import os
import pandas as pd

def save_csv(dataframe, file_path):
    """
    Guarda un DataFrame en un archivo CSV.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    dataframe.to_csv(file_path, index=False)
    print(f"Archivo guardado en: {file_path}")

def load_csv(file_path):
    """
    Carga un archivo CSV en un DataFrame.
    """
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        raise FileNotFoundError(f"No se encontró el archivo: {file_path}")
