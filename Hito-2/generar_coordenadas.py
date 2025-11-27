"""
Script simple para generar coordenadas desde el CSV de intervenciones
"""

import pandas as pd
import numpy as np

# Coordenadas reales de capitales de departamento del Perú
COORDS_DEPARTAMENTOS = {
    'TACNA': (-18.0146, -70.2502),
    'AREQUIPA': (-16.4090, -71.5375),
    'MOQUEGUA': (-17.1934, -70.9346),
    'PUNO': (-15.8402, -70.0219),
    'CUSCO': (-13.5319, -71.9675),
    'APURIMAC': (-13.6339, -73.3641),
    'AYACUCHO': (-13.1631, -74.2236),
    'ICA': (-14.0678, -75.7286),
    'HUANCAVELICA': (-12.7869, -74.9760),
    'JUNIN': (-12.0689, -75.2048),
    'LIMA': (-12.0464, -77.0428),
    'PASCO': (-10.6819, -76.2578),
    'HUANUCO': (-9.9307, -76.2422),
    'UCAYALI': (-8.3791, -74.5539),
    'SAN MARTIN': (-6.4869, -76.3650),
    'AMAZONAS': (-5.7698, -77.8700),
    'LORETO': (-3.7437, -73.2516),
    'CAJAMARCA': (-7.1638, -78.5128),
    'LA LIBERTAD': (-8.1116, -79.0289),
    'ANCASH': (-9.5278, -77.5278),
    'LAMBAYEQUE': (-6.7714, -79.8391),
    'PIURA': (-5.1945, -80.6328),
    'TUMBES': (-3.5668, -80.4515),
    'MADRE DE DIOS': (-12.5931, -69.1891),
}

def generar_desde_csv(archivo_csv, archivo_salida, num_puntos=50):
    """Genera coordenadas desde el CSV"""

    print(f"📂 Cargando {archivo_csv}...")

    # Cargar CSV
    df = pd.read_csv(archivo_csv, sep=';', encoding='latin1')
    print(f"✓ {len(df)} registros cargados")

    # Obtener rutas únicas limitadas
    print(f"\n🛣️ Procesando rutas (limitado a {num_puntos})...")
    rutas_unicas = df.drop_duplicates(subset=['CODIGO_RUTA']).head(num_puntos)

    coordenadas = []
    nombres = []

    np.random.seed(42)  # Para reproducibilidad

    for idx, row in rutas_unicas.iterrows():
        try:
            codigo_ruta = str(row['CODIGO_RUTA'])
            dept_raw = str(row['DEPARTAMENTO'])
            provincia = str(row['PROVINCIA'])

            # Limpiar departamento
            dept = dept_raw.strip().upper()
            if '-' in dept:
                dept = dept.split('-')[0].strip()

            # Buscar coordenadas
            if dept in COORDS_DEPARTAMENTOS:
                base_lat, base_lon = COORDS_DEPARTAMENTOS[dept]

                # Añadir variación aleatoria
                lat = base_lat + np.random.uniform(-0.3, 0.3)
                lon = base_lon + np.random.uniform(-0.3, 0.3)

                coordenadas.append([lat, lon])
                nombres.append(f"{codigo_ruta}_{provincia[:20]}")

        except Exception as e:
            print(f"⚠️ Error en fila {idx}: {e}")
            continue

    print(f"✓ Generadas {len(coordenadas)} coordenadas")

    # Crear DataFrame
    df_coordenadas = pd.DataFrame({
        'Nombre': nombres,
        'Latitud': [c[0] for c in coordenadas],
        'Longitud': [c[1] for c in coordenadas]
    })

    # Guardar
    print(f"\n💾 Guardando en {archivo_salida}...")
    df_coordenadas.to_excel(archivo_salida, index=False)
    print(f"✓ Archivo guardado")

    # Mostrar resumen
    print(f"\n📊 RESUMEN:")
    print(f"  Total de puntos: {len(df_coordenadas)}")
    print(f"  Rango latitud: [{df_coordenadas['Latitud'].min():.4f}, {df_coordenadas['Latitud'].max():.4f}]")
    print(f"  Rango longitud: [{df_coordenadas['Longitud'].min():.4f}, {df_coordenadas['Longitud'].max():.4f}]")
    print(f"\n✅ Primeros 5 registros:")
    print(df_coordenadas.head())

    return df_coordenadas


if __name__ == '__main__':
    print("=" * 70)
    print("🚀 GENERADOR DE COORDENADAS")
    print("=" * 70)

    # Generar coordenadas
    df_resultado = generar_desde_csv(
        '1_Dataset_Intervenciones_PVD_30062025.csv',
        'dataset_tp_complejidad.xlsx',
        num_puntos=50
    )

    print("\n" + "=" * 70)
    print("✅ PROCESO COMPLETADO")
    print("=" * 70)
    print("\nAhora puedes ejecutar el sistema de optimización con:")
    print("  python main.py")

