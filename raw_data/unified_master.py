import pandas as pd

def crear_dataset_maestro(ruta_violencia, ruta_divorcios, ruta_salida):
    print("Cargando y preparando datos...")
    
    # 1. Cargar archivos limpios
    df_v = pd.read_csv(ruta_violencia, sep=';', low_memory=False)
    df_d = pd.read_csv(ruta_divorcios, sep=';', low_memory=False)

    # 2. Traducción de códigos en Divorcios (Vital para que coincidan con Violencia)
    mapa_deptos = {
        1: 'Guatemala', 2: 'El Progreso', 3: 'Sacatepéquez', 4: 'Chimaltenango',
        5: 'Escuintla', 6: 'Santa Rosa', 7: 'Sololá', 8: 'Totonicapán',
        9: 'Quetzaltenango', 10: 'Suchitepéquez', 11: 'Retalhuleu', 12: 'San Marcos',
        13: 'Huehuetenango', 14: 'Quiché', 15: 'Baja Verapaz', 16: 'Alta Verapaz',
        17: 'Petén', 18: 'Izabal', 19: 'Zacapa', 20: 'Chiquimula', 21: 'Jalapa', 22: 'Jutiapa'
    }
    
    # Aplicar traducción y estandarizar nombres de columnas comunes
    df_d['DEPTO'] = df_d['DEPTO'].map(mapa_deptos)
    
    # 3. Estandarizar columnas comunes para el "Match"
    # Renombramos DEPTOMCPIO de violencia a solo DEPTO para que se alineen
    df_v = df_v.rename(columns={'DEPTOMCPIO': 'DEPTO'})

    # 4. AGREGAR ETIQUETA DE EVENTO (Esta es la clave)
    df_v['TIPO_EVENTO'] = 'Denuncia Violencia'
    df_d['TIPO_EVENTO'] = 'Divorcio'

    # 5. CONCATENACIÓN (Apilar tablas)
    # Pandas alineará ANO, MES, DEPTO y DIA automáticamente.
    # El resto de columnas (como TIPAGRE o EDAD_HOM) quedarán con NaN donde no apliquen.
    print("Concatenando datasets...")
    df_master = pd.concat([df_v, df_d], axis=0, ignore_index=True, sort=False)

    # 6. Limpieza final del Master
    # Eliminar años fuera de rango (como los 200 o 9999 que vimos antes)
    df_master = df_master[(df_master['ANO'] >= 2009) & (df_master['ANO'] <= 2022)]

    # 7. Guardar el archivo final
    df_master.to_csv(ruta_salida, index=False, sep=';', encoding='utf-8-sig')
    
    print("-" * 30)
    print(f"¡DATASET MAESTRO CREADO!")
    print(f"Archivo: {ruta_salida}")
    print(f"Registros totales: {len(df_master)}")
    print(f"Columnas totales: {len(df_master.columns)}")

if __name__ == "__main__":
    crear_dataset_maestro(
        '../data/files/Violencia_Intrafamiliar_Limpio.csv', 
        '../data/files/Divorcios_Limpio.csv', 
        '../data/files/Dataset_Unificado_Proyecto.csv'
    )