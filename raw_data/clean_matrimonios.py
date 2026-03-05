import pandas as pd
import numpy as np

def limpiar_matrimonios(ruta_input, ruta_output):
    print("Cargando dataset de matrimonios consolidado...")
    
    df = pd.read_csv(ruta_input, sep=';', encoding='utf-8')

    # 1️⃣ NORMALIZAR NOMBRES DE COLUMNAS
    df.columns = (
        df.columns
        .str.upper()
        .str.strip()
        .str.replace("�", "N", regex=False)
    )

    df = df.loc[:, ~df.columns.duplicated()]
    
    print("Columnas detectadas:")
    print(df.columns.tolist())

    # 2️⃣ LIMPIEZA DE TEXTO
    columnas_texto = [
        'DEPREG', 'MUPREG', 'MESREG', 'CLAUNI',
        'GETHOM', 'GETMUJ', 'NACHOM', 'NACMUJ',
        'OCUHOM', 'OCUMUJ', 'DEPOCU', 'MUPOCU',
        'MESOCU', 'AREAG'
    ]

    for col in columnas_texto:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.title()
            )

    # 3️⃣ CONVERTIR NUMÉRICOS
    columnas_numericas = [
        'ANOREG', 'EDADHOM', 'EDADMUJ',
        'NUPHON', 'NUPMUJ', 'ANOOCU'
    ]

    for col in columnas_numericas:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    print("Conversión numérica completada.")

    # 4️⃣ ELIMINAR DUPLICADOS
    antes = len(df)
    df = df.drop_duplicates()
    print(f"Registros únicos finales: {len(df)} (Eliminados {antes - len(df)} duplicados)")

    # 5️⃣ AGREGAR IDENTIFICADOR
    df['TIPO_EVENTO_REAL'] = 'Matrimonio'

    # 6️⃣ GUARDAR RESULTADO
    df.to_csv(ruta_output, index=False, sep=';', encoding='utf-8-sig')

    df = pd.read_csv(ruta_input, sep=';', encoding='utf-8', low_memory=False)

    print("-" * 40)
    print("PROCESO COMPLETADO")
    print(f"Archivo guardado en: {ruta_output}")


if __name__ == "__main__":
    INPUT = '../data/files/Matrimonios_Consolidado.csv'
    OUTPUT = '../data/files/matrimonios/matrimonios_limpio.csv'

    limpiar_matrimonios(INPUT, OUTPUT)