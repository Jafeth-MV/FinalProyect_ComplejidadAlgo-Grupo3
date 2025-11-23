"""
Procesamiento y geocodificación del dataset de Provías.
Convierte direcciones textuales a coordenadas geográficas.
"""

import pandas as pd
import numpy as np
from typing import Tuple, List, Dict
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time


class DatasetProcessor:
    """
    Procesa el dataset de Provías y realiza geocodificación.
    """

    def __init__(self, excel_path: str):
        self.excel_path = excel_path
        self.df_original = None
        self.df_procesado = None
        self.geolocator = Nominatim(user_agent="rutafix_app", timeout=10)

    def cargar_dataset(self) -> pd.DataFrame:
        """Carga el dataset desde Excel."""
        print(f"Cargando dataset desde: {self.excel_path}")
        self.df_original = pd.read_excel(self.excel_path)
        print(f"✓ Dataset cargado: {len(self.df_original)} filas")
        print(f"✓ Columnas: {list(self.df_original.columns)}")
        return self.df_original

    def limpiar_dataset(self) -> pd.DataFrame:
        """
        Limpia y normaliza el dataset.
        Filtra columnas relevantes y maneja valores faltantes.
        """
        print("\nLimpiando dataset...")

        # Identificar columnas relevantes
        columnas_esperadas = {
            'TRAMO': ['TRAMO', 'Tramo', 'tramo'],
            'PROVINCIA': ['PROVINCIA', 'Provincia', 'provincia'],
            'DISTRITO': ['DISTRITO', 'Distrito', 'distrito'],
            'DEPARTAMENTO': ['DEPARTAMENTO', 'Departamento', 'departamento'],
            'INICIO': ['INICIO', 'Inicio', 'inicio', 'KM_INICIO'],
            'FIN': ['FIN', 'Fin', 'fin', 'KM_FIN']
        }

        # Mapear columnas
        columnas_mapeadas = {}
        for key, posibles in columnas_esperadas.items():
            for col in self.df_original.columns:
                if col in posibles:
                    columnas_mapeadas[col] = key
                    break

        # Crear dataframe limpio
        self.df_procesado = self.df_original.rename(columns=columnas_mapeadas)

        # Eliminar filas con datos faltantes en columnas críticas
        columnas_criticas = ['TRAMO', 'PROVINCIA']
        self.df_procesado = self.df_procesado.dropna(subset=columnas_criticas)

        print(f"✓ Dataset limpio: {len(self.df_procesado)} filas válidas")
        return self.df_procesado

    def geocodificar_direcciones(self, limite: int = None,
                                delay: float = 1.0) -> pd.DataFrame:
        """
        Geocodifica las direcciones del dataset a coordenadas.

        Args:
            limite: Número máximo de direcciones a geocodificar (None = todas)
            delay: Tiempo de espera entre peticiones (segundos)

        Returns:
            DataFrame con columnas Latitud y Longitud agregadas
        """
        print("\nIniciando geocodificación...")

        if self.df_procesado is None:
            raise ValueError("Primero debe limpiar el dataset")

        # Limitar número de geocodificaciones si se especifica
        df_geo = self.df_procesado.copy()
        if limite:
            df_geo = df_geo.head(limite)
            print(f"Geocodificando primeras {limite} direcciones...")

        latitudes = []
        longitudes = []
        errores = 0

        total = len(df_geo)

        for idx, row in df_geo.iterrows():
            # Construir dirección
            direccion_parts = []

            if pd.notna(row.get('TRAMO')):
                direccion_parts.append(str(row['TRAMO']))
            if pd.notna(row.get('DISTRITO')):
                direccion_parts.append(str(row['DISTRITO']))
            if pd.notna(row.get('PROVINCIA')):
                direccion_parts.append(str(row['PROVINCIA']))
            if pd.notna(row.get('DEPARTAMENTO')):
                direccion_parts.append(str(row['DEPARTAMENTO']))
            else:
                direccion_parts.append('Perú')

            direccion = ', '.join(direccion_parts)

            # Intentar geocodificar
            try:
                location = self.geolocator.geocode(direccion)

                if location:
                    latitudes.append(location.latitude)
                    longitudes.append(location.longitude)
                else:
                    latitudes.append(np.nan)
                    longitudes.append(np.nan)
                    errores += 1

                # Mostrar progreso
                if (idx + 1) % 10 == 0:
                    progreso = (idx + 1) / total * 100
                    print(f"  Progreso: {progreso:.1f}% ({idx + 1}/{total})")

                # Esperar para no sobrecargar el servicio
                time.sleep(delay)

            except (GeocoderTimedOut, GeocoderServiceError) as e:
                print(f"  Error en índice {idx}: {e}")
                latitudes.append(np.nan)
                longitudes.append(np.nan)
                errores += 1
                time.sleep(delay * 2)  # Esperar más después de un error

        # Agregar coordenadas al dataframe
        df_geo['Latitud'] = latitudes
        df_geo['Longitud'] = longitudes
        df_geo['Nodo'] = [f"Nodo_{i}" for i in range(len(df_geo))]

        # Eliminar filas sin coordenadas
        df_geo = df_geo.dropna(subset=['Latitud', 'Longitud'])

        print(f"\n✓ Geocodificación completada")
        print(f"  Total procesado: {total}")
        print(f"  Exitosos: {total - errores}")
        print(f"  Errores: {errores}")
        print(f"  Válidos finales: {len(df_geo)}")

        self.df_procesado = df_geo
        return df_geo

    def usar_coordenadas_simuladas(self, centro_lat: float = -12.0462,
                                   centro_lon: float = -77.0428,
                                   radio: float = 0.5) -> pd.DataFrame:
        """
        Genera coordenadas simuladas alrededor de un centro (para pruebas rápidas).

        Args:
            centro_lat: Latitud del centro (por defecto Lima)
            centro_lon: Longitud del centro
            radio: Radio de dispersión en grados

        Returns:
            DataFrame con coordenadas simuladas
        """
        print("\nGenerando coordenadas simuladas...")

        if self.df_procesado is None:
            raise ValueError("Primero debe limpiar el dataset")

        n = len(self.df_procesado)

        # Generar coordenadas aleatorias alrededor del centro
        np.random.seed(42)
        latitudes = centro_lat + (np.random.randn(n) * radio)
        longitudes = centro_lon + (np.random.randn(n) * radio)

        self.df_procesado['Latitud'] = latitudes
        self.df_procesado['Longitud'] = longitudes
        self.df_procesado['Nodo'] = [f"Nodo_{i}" for i in range(n)]

        print(f"✓ Coordenadas simuladas generadas para {n} puntos")
        print(f"  Centro: ({centro_lat}, {centro_lon})")
        print(f"  Radio: {radio} grados")

        return self.df_procesado

    def exportar_procesado(self, output_path: str):
        """Exporta el dataset procesado a Excel."""
        if self.df_procesado is None:
            raise ValueError("No hay dataset procesado para exportar")

        self.df_procesado.to_excel(output_path, index=False)
        print(f"✓ Dataset procesado exportado a: {output_path}")

    def obtener_coordenadas(self) -> Tuple[np.ndarray, List[str]]:
        """
        Obtiene las coordenadas y nombres del dataset procesado.

        Returns:
            Tupla (coordenadas, nombres)
        """
        if self.df_procesado is None:
            raise ValueError("No hay dataset procesado")

        coordenadas = self.df_procesado[['Latitud', 'Longitud']].values
        nombres = self.df_procesado['Nodo'].tolist()

        return coordenadas, nombres


def procesar_dataset_provias(input_path: str, output_path: str,
                             usar_simulacion: bool = True,
                             limite_geocoding: int = None) -> pd.DataFrame:
    """
    Función principal para procesar el dataset de Provías.

    Args:
        input_path: Ruta al archivo Excel de entrada
        output_path: Ruta para guardar el dataset procesado
        usar_simulacion: Si True, usa coordenadas simuladas en lugar de geocodificar
        limite_geocoding: Límite de direcciones a geocodificar (si no se usa simulación)

    Returns:
        DataFrame procesado
    """
    print("="*70)
    print("PROCESAMIENTO DE DATASET - PROVÍAS")
    print("="*70)

    processor = DatasetProcessor(input_path)

    # Cargar y limpiar
    processor.cargar_dataset()
    processor.limpiar_dataset()

    # Obtener coordenadas
    if usar_simulacion:
        df_final = processor.usar_coordenadas_simuladas()
    else:
        df_final = processor.geocodificar_direcciones(limite=limite_geocoding)

    # Exportar
    processor.exportar_procesado(output_path)

    print("\n" + "="*70)
    print("PROCESAMIENTO COMPLETADO")
    print("="*70)

    return df_final


if __name__ == "__main__":
    # Ejemplo de uso
    print("\nMódulo de Procesamiento de Dataset")
    print("="*50)
    print("Funcionalidades:")
    print("1. Carga y limpieza de datos de Provías")
    print("2. Geocodificación de direcciones")
    print("3. Generación de coordenadas simuladas")
    print("4. Exportación de datos procesados")
    print("="*50)

