

import pandas as pd
import numpy as np
import sys

print("Iniciando generador...")

try:
    # Coordenadas
    COORDS = {
        'TACNA': (-18.0146, -70.2502),
        'AREQUIPA': (-16.4090, -71.5375),
        'MOQUEGUA': (-17.1934, -70.9346),
        'PUNO': (-15.8402, -70.0219),
        'CUSCO': (-13.5319, -71.9675),
    }

    print("Cargando CSV...")
    df = pd.read_csv('1_Dataset_Intervenciones_PVD_30062025.csv',
                     sep=';',
                     encoding='latin1',
                     nrows=100)  # Solo las primeras 100 filas

    print(f"CSV cargado: {len(df)} filas")
    print(f"Columnas: {df.columns.tolist()}")

    # Generar coordenadas
    nombres = []
    lats = []
    lons = []

    np.random.seed(42)

    for i, row in df.iterrows():
        try:
            codigo = str(row['CODIGO_RUTA'])
            dept = str(row['DEPARTAMENTO']).strip().upper().split('-')[0].strip()

            if dept in COORDS:
                lat, lon = COORDS[dept]
                lat += np.random.uniform(-0.2, 0.2)
                lon += np.random.uniform(-0.2, 0.2)

                nombres.append(f"Ruta_{i}_{codigo}")
                lats.append(lat)
                lons.append(lon)

                if len(nombres) >= 50:
                    break
        except:
            continue

    print(f"Generadas {len(nombres)} coordenadas")

    # Crear DataFrame
    df_out = pd.DataFrame({
        'Nombre': nombres,
        'Latitud': lats,
        'Longitud': lons
    })

    # Guardar
    archivo_salida = 'dataset_tp_complejidad.xlsx'
    print(f"Guardando en {archivo_salida}...")
    df_out.to_excel(archivo_salida, index=False)

    print(f"Archivo guardado exitosamente")
    print(f"\nPrimeros 5 registros:")
    print(df_out.head())

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

