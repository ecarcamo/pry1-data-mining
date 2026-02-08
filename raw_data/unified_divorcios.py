import pandas as pd
import os

def unificar_csv_divorcios(carpeta_input, archivo_salida):
    archivos = [f for f in os.listdir(carpeta_input) if f.endswith('.csv')]
    lista_df = []
    
    # Mapeo de normalización para columnas que cambian de nombre/formato
    mapeo_columnas = {
        'añoreg': 'AÑOREG', 'añoocu': 'AÑOOCU', 'escohom': 'ESCHOM', 
        'escomuj': 'ESCMUJ', 'ocupahom': 'CIUOHOM', 'ocupamuj': 'CIUOMUJ',
        'grethom': 'PPERHOM', 'gretmuj': 'PPERMUJ', 'gethom': 'PPERHOM', 
        'getmuj': 'PPERMUJ', 'puehom': 'PPERHOM', 'puemuj': 'PPERMUJ',
        'puehom': 'PPERHOM', 'puemuj': 'PPERMUJ'
    }

    for archivo in archivos:
        print(f"Procesando: {archivo}")
        # Leer archivo (usamos sep=';' por el formato del INE)
        df = pd.read_csv(os.path.join(carpeta_input, archivo), sep=';', low_memory=False)
        
        # 1. Todo a mayúsculas para evitar 'Edad' vs 'EDAD'
        df.columns = [col.upper() for col in df.columns]
        
        # 2. Quitar tildes y eñes en los nombres de columnas para estandarizar
        df.columns = [col.replace('AÑOREG', 'ANOREG').replace('AÑOOCU', 'ANOOCU') for col in df.columns]
        
        # 3. Aplicar mapeo de sinónimos
        df.rename(columns=mapeo_columnas, inplace=True)
        
        lista_df.append(df)

    # Concatenar todos
    df_final = pd.concat(lista_df, ignore_index=True)
    
    # Quitar filas duplicadas exactas
    antes = len(df_final)
    df_final = df_final.drop_duplicates()
    
    # Guardar resultado
    df_final.to_csv(archivo_salida, index=False, sep=';', encoding='utf-8-sig')
    print(f"\n¡Unificación exitosa!")
    print(f"Filas originales: {antes} -> Filas únicas: {len(df_final)}")
    print(f"Archivo guardado como: {archivo_salida}")

# Uso del script
unificar_csv_divorcios('./files/divorcios', '../data/files/Divorcios_Consolidado.csv')