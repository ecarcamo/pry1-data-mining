import pandas as pd

def limpiar_divorcios_final(ruta_input, ruta_output):
    df = pd.read_csv(ruta_input, sep=';', low_memory=False)
    
    # 1. Fusionar Etnias
    for sexo in ['HOM', 'MUJ']:
        df[f'ETNIA_{sexo}'] = df[f'PPER{sexo}'].fillna(df[f'PUE{sexo}']).fillna(df[f'GRET{sexo}']).fillna(df[f'GET{sexo}'])
        # 2. Fusionar Escolaridad
        df[f'ESC_{sexo}'] = df[f'ESC{sexo}'].fillna(df[f'ESCO{sexo}'])
        # 3. Fusionar Ocupación
        df[f'OCU_{sexo}'] = df[f'CIUO{sexo}'].fillna(df[f'OCUPA{sexo}']).fillna(df[f'OCU{sexo}'])

    # 4. Seleccionar solo lo importante y renombrar para quitar el 'OCU'
    columnas_map = {
        'ANOOCU': 'ANO',
        'MESOCU': 'MES',
        'DIAOCU': 'DIA',
        'DEPOCU': 'DEPTO',
        'MUPOCU': 'MUNICIPIO',
        'EDADHOM': 'EDAD_HOM',
        'EDADMUJ': 'EDAD_MUJ',
        'ETNIA_HOM': 'ETNIA_HOM',
        'ETNIA_MUJ': 'ETNIA_MUJ',
        'ESC_HOM': 'ESCOLARIDAD_HOM',
        'ESC_MUJ': 'ESCOLARIDAD_MUJ',
        'OCU_HOM': 'OCUPACION_HOM',
        'OCU_MUJ': 'OCUPACION_MUJ'
    }
    
    df_limpio = df[list(columnas_map.keys())].rename(columns=columnas_map)
    
    # 5. Eliminar duplicados y guardar
    df_limpio = df_limpio.drop_duplicates()
    df_limpio.to_csv(ruta_output, index=False, sep=';', encoding='utf-8-sig')
    print(f"Limpieza terminada. Columnas finales: {df_limpio.columns.tolist()}")

if __name__ == "__main__":
    limpiar_divorcios_final('../data/files/Divorcios_Consolidado.csv', '../data/files/Divorcios_Limpio.csv')