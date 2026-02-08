import pandas as pd
import numpy as np

def limpiar_y_unificar_data(ruta_input, ruta_output):
    print("Cargando dataset consolidado...")
    df = pd.read_csv(ruta_input, sep=';', low_memory=False)
    
    # 1. FUSIONAR COLUMNAS "SINÓNIMAS" antes de filtrar
    if 'AGR_GURPET' in df.columns:
        df['AGR_GRUPET'] = df['AGR_GRUPET'].fillna(df['AGR_GURPET'])
    
    # 2. SELECCIÓN DE COLUMNAS ESENCIALES
    columnas_a_mantener = [
        'HEC_ANO', 'HEC_MES', 'HEC_DIA', 'HEC_DEPTOMCPIO', 'HEC_AREA',
        'VIC_SEXO', 'VIC_EDAD', 'VIC_EST_CIV', 'VIC_ESCOLARIDAD', 
        'VIC_REL_AGR', 'TOTAL_HIJOS', 'AGR_SEXO', 'AGR_EDAD', 
        'AGR_GRUPET', 'HEC_TIPAGRE', 'LEY_APLICABLE', 'HEC_RECUR_DENUN'
    ]
    
    # Filtrar solo las que existen
    df_limpio = df[[col for col in columnas_a_mantener if col in df.columns]].copy()

    # 3. QUITAR PREFIJOS "HEC_"
    # Esto hace que 'HEC_ANO' pase a ser solo 'ANO', etc.
    df_limpio.columns = [col.replace('HEC_', '') for col in df_limpio.columns]
    print("Prefijos 'HEC_' eliminados de las columnas.")

    # 4. LIMPIEZA DE TIPOS DE DATOS (Usando los nuevos nombres sin prefijo)
    print("Ajustando tipos de datos numéricos...")
    # 'ANO' y 'DIA' ahora no tienen el prefijo
    cols_numericas = ['ANO', 'DIA', 'VIC_EDAD', 'AGR_EDAD', 'TOTAL_HIJOS']
    for col in cols_numericas:
        if col in df_limpio.columns:
            df_limpio[col] = pd.to_numeric(df_limpio[col], errors='coerce')

    # 5. ELIMINACIÓN DE DUPLICADOS
    antes = len(df_limpio)
    df_limpio = df_limpio.drop_duplicates()
    print(f"Registros únicos finales: {len(df_limpio)} (Se eliminaron {antes - len(df_limpio)} duplicados)")

    # 6. GUARDAR RESULTADO
    df_limpio.to_csv(ruta_output, index=False, sep=';', encoding='utf-8-sig')
    
    print("-" * 30)
    print(f"PROCESO COMPLETADO")
    print(f"Columnas finales: {df_limpio.columns.tolist()}")
    print(f"Archivo guardado en: {ruta_output}")

if __name__ == "__main__":
    INPUT = './files/violencia_intrafamiliar/Violencia_Intrafamiliar_Consolidado.csv'
    OUTPUT = '../data/files/Violencia_Intrafamiliar_Limpio.csv'
    
    limpiar_y_unificar_data(INPUT, OUTPUT)