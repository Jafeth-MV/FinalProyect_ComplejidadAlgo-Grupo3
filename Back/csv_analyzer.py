import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import time
import pickle
import os

class CSVAnalyzer:

    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.df = None
        self.coordenadas_cache = {}
        self.cache_file = 'coordenadas_cache.pkl'

    def cargar_csv(self):
        print("Cargando CSV...")
        try:
            # Intentar diferentes encodings
            for encoding in ['latin1', 'iso-8859-1', 'cp1252', 'utf-8']:
                try:
                    self.df = pd.read_csv(self.csv_path, sep=';', encoding=encoding)
                    print(f"CSV cargado con encoding {encoding}")
                    print(f"  Total de registros: {len(self.df)}")
                    print(f"  Columnas: {list(self.df.columns)}")
                    return True
                except:
                    continue
            print("No se pudo cargar el CSV con ningún encoding")
            return False
        except Exception as e:
            print(f"Error al cargar CSV: {e}")
            return False

    def analizar_estructura(self):
        if self.df is None:
            print("Primero debes cargar el CSV")
            return

        print("\nANÁLISIS DEL CSV")
        print("=" * 60)
        print(f"Total de registros: {len(self.df)}")
        print(f"\nColumnas ({len(self.df.columns)}):")
        for i, col in enumerate(self.df.columns, 1):
            print(f"  {i}. {col}")

        print("\nINFORMACIÓN GEOGRÁFICA DISPONIBLE:")
        print(f"  - Departamentos únicos: {self.df['DEPARTAMENTO'].nunique()}")
        print(f"  - Provincias únicas: {self.df['PROVINCIA'].nunique()}")

        print("\nPrimeros registros:")
        print(self.df[['CODIGO_RUTA', 'DEPARTAMENTO', 'PROVINCIA', 'INICIO', 'FINAL', 'LONGITUD']].head(10))

    def cargar_cache(self):
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'rb') as f:
                    self.coordenadas_cache = pickle.load(f)
                print(f"Cache cargado: {len(self.coordenadas_cache)} ubicaciones")
            except:
                print("No se pudo cargar el cache")

    def guardar_cache(self):
        try:
            with open(self.cache_file, 'wb') as f:
                pickle.dump(self.coordenadas_cache, f)
            print(f"Cache guardado: {len(self.coordenadas_cache)} ubicaciones")
        except Exception as e:
            print(f"Error al guardar cache: {e}")

    def obtener_coordenadas_provincia(self, departamento, provincia):
        key = f"{departamento}_{provincia}"

        # Verificar cache
        if key in self.coordenadas_cache:
            return self.coordenadas_cache[key]

        # Geocoding (lento, por eso usamos cache)
        try:
            geolocator = Nominatim(user_agent="route_optimizer")
            location = geolocator.geocode(f"{provincia}, {departamento}, Peru")

            if location:
                coords = (location.latitude, location.longitude)
                self.coordenadas_cache[key] = coords
                time.sleep(1)  # Respetar límites de la API
                return coords
            else:
                print(f"No se encontraron coordenadas para {provincia}, {departamento}")
                return None
        except Exception as e:
            print(f"Error en geocoding: {e}")
            return None

    def generar_coordenadas_aproximadas(self):
        if self.df is None:
            print("Primero debes cargar el CSV")
            return None

        print("\nGenerando coordenadas aproximadas...")
        self.cargar_cache()

        # Coordenadas aproximadas de capitales de departamento (Perú)
        coords_departamentos = {
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
            'MADRE DE DIOS': (-12.5931, -69.1891)
        }

        coordenadas = []
        nombres = []

        # Obtener registros únicos por provincia
        provincias_unicas = self.df[['DEPARTAMENTO', 'PROVINCIA']].drop_duplicates()

        print(f"  Procesando {len(provincias_unicas)} ubicaciones únicas...")

        for idx, row in provincias_unicas.iterrows():
            dept = row['DEPARTAMENTO']
            prov = row['PROVINCIA']

            # Usar coordenadas del departamento como base
            if dept in coords_departamentos:
                base_lat, base_lon = coords_departamentos[dept]

                # Añadir variación aleatoria pequeña para cada provincia
                lat = base_lat + np.random.uniform(-0.5, 0.5)
                lon = base_lon + np.random.uniform(-0.5, 0.5)

                coordenadas.append([lat, lon])
                nombres.append(f"{prov} ({dept})")

        self.guardar_cache()

        print(f"Generadas {len(coordenadas)} coordenadas")
        return np.array(coordenadas), nombres

    def generar_coordenadas_por_ruta(self, max_rutas=100):
        if self.df is None:
            print("Primero debes cargar el CSV")
            return None

        print(f"\nGenerando coordenadas por ruta (max: {max_rutas})...")

        # Coordenadas base por departamento
        coords_departamentos = {
            'TACNA': (-18.0146, -70.2502),
            'AREQUIPA': (-16.4090, -71.5375),
            'MOQUEGUA': (-17.1934, -70.9346),
            'PUNO': (-15.8402, -70.0219),
            'CUSCO': (-13.5319, -71.9675),
        }

        # Agrupar por código de ruta
        rutas_unicas = self.df.groupby('CODIGO_RUTA').first().head(max_rutas)

        coordenadas = []
        nombres = []

        for codigo_ruta, row in rutas_unicas.iterrows():
            dept = str(row['DEPARTAMENTO']).strip().upper()

            # Limpiar nombre del departamento (puede tener múltiples)
            if '-' in dept:
                dept = dept.split('-')[0].strip()

            # Si el departamento tiene múltiples registros, distribuirlos
            if dept in coords_departamentos:
                base_lat, base_lon = coords_departamentos[dept]

                # Variación basada en la longitud de la ruta
                try:
                    longitud_km = float(row['LONGITUD'])
                    # Más longitud = más dispersión (aproximación)
                    variacion = min(longitud_km / 100, 1.0)
                except:
                    variacion = 0.3

                lat = base_lat + np.random.uniform(-variacion, variacion)
                lon = base_lon + np.random.uniform(-variacion, variacion)

                coordenadas.append([lat, lon])
                nombres.append(f"{codigo_ruta}")

        print(f"Generadas {len(coordenadas)} coordenadas de rutas")
        return np.array(coordenadas), nombres

    def exportar_a_excel(self, coordenadas, nombres, archivo='dataset_coordenadas.xlsx'):
        print(f"\nExportando a {archivo}...")

        df_export = pd.DataFrame({
            'Nombre': nombres,
            'Latitud': coordenadas[:, 0],
            'Longitud': coordenadas[:, 1]
        })

        df_export.to_excel(archivo, index=False)
        print(f"Archivo exportado: {archivo}")


def main():
    print("=" * 70)
    print("ANALIZADOR DE CSV - SISTEMA DE OPTIMIZACIÓN DE RUTAS")
    print("=" * 70)

    # Ruta al CSV
    csv_path = '1_Dataset_Intervenciones_PVD_30062025.csv'

    # Crear analizador
    analyzer = CSVAnalyzer(csv_path)

    # Cargar y analizar
    if not analyzer.cargar_csv():
        return

    analyzer.analizar_estructura()

    # Generar coordenadas
    print("\n" + "=" * 70)
    print("OPCIONES DE GENERACIÓN DE COORDENADAS")
    print("=" * 70)

    # Opción 1: Por provincias
    coords1, nombres1 = analyzer.generar_coordenadas_aproximadas()
    if coords1 is not None and len(coords1) > 0:
        analyzer.exportar_a_excel(coords1, nombres1, 'dataset_provincias.xlsx')

    # Opción 2: Por rutas (limitado a 100)
    coords2, nombres2 = analyzer.generar_coordenadas_por_ruta(max_rutas=100)
    if coords2 is not None and len(coords2) > 0:
        analyzer.exportar_a_excel(coords2, nombres2, 'dataset_rutas.xlsx')

    print("\n" + "=" * 70)
    print("ANÁLISIS COMPLETADO")
    print("=" * 70)
    print("\nArchivos generados:")
    print("  1. dataset_provincias.xlsx - Coordenadas por provincia")
    print("  2. dataset_rutas.xlsx - Coordenadas por ruta (max 100)")
    print("\nEstos archivos pueden ser usados por el sistema de optimización.")


if __name__ == '__main__':
    main()
