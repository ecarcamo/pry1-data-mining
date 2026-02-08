import pandas as pd
import os
from pathlib import Path

def unificar_violencia_excel(directorio_fuente, archivo_salida):
    ruta_base = Path(directorio_fuente)

    archivos_excel = list(ruta_base.glob("*.xlsx"))
    
    if not archivos_excel:
        print(f"No se encontraron archivos Excel en {directorio_fuente}")
        return

    lista_dataframes = []

    for archivo in archivos_excel:
        print(f"Leyendo: {archivo.name}...")
        try:
            df = pd.read_excel(archivo, engine='openpyxl')
            
            df['ORIGEN_DATOS'] = archivo.name
            
            lista_dataframes.append(df)
        except Exception as e:
            print(f"Error al leer {archivo.name}: {e}")

    print("\nCombinando archivos y alineando columnas...")
    df_unificado = pd.concat(lista_dataframes, axis=0, ignore_index=True, sort=False)

    filas_antes = len(df_unificado)
    df_unificado = df_unificado.drop_duplicates()
    filas_despues = len(df_unificado)

    print(f"Duplicados eliminados: {filas_antes - filas_despues}")
    
    df_unificado.to_csv(archivo_salida, index=False, sep=';', encoding='utf-8-sig')
    
    print("-" * 30)
    print(f"PROCESO COMPLETADO")
    print(f"Archivo final: {archivo_salida}")
    print(f"Total de registros únicos: {filas_despues}")
    print(f"Total de columnas (incluyendo nuevas): {len(df_unificado.columns)}")

if __name__ == "__main__":
    unificar_violencia_excel("files/violencia_intrafamiliar", "../data/files/Violencia_Intrafamiliar_Consolidado.csv")