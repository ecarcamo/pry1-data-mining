import pandas as pd
import pyreadstat
import os
from pathlib import Path

def process_divorce_folder(folder_path):
    directory = Path(folder_path)
    
    sav_files = list(directory.glob("*.sav"))
    
    if not sav_files:
        print(f"No se encontraron archivos .sav en {folder_path}")
        return

    for sav_file in sav_files:
        try:
            df, meta = pyreadstat.read_sav(str(sav_file))
            
            csv_file = sav_file.with_suffix('.csv')
            
            df.to_csv(csv_file, index=False, sep=';') # Usamos ';' por consistencia con tus archivos previos
            print(f"Convertido: {sav_file.name} -> {csv_file.name}")
            
            os.remove(sav_file)
            print(f"Archivo original {sav_file.name} eliminado.")
            
        except Exception as e:
            print(f"Error procesando {sav_file.name}: {e}")

if __name__ == "__main__":
    ruta_divorcios = "files/divorcios/" 
    process_divorce_folder(ruta_divorcios)