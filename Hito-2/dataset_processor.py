"""
Dataset Processor
Procesa datasets de Excel con coordenadas y nombres de lugares
"""

import pandas as pd
import numpy as np
from typing import Tuple, List, Optional
from geopy.distance import geodesic


class DatasetProcessor:
    """
    Procesa datasets de coordenadas desde archivos Excel.
    """

    def __init__(self):
        self.df = None
        self.coordenadas = None
        self.nombres = None

    def cargar_desde_excel(
        self,
        archivo: str,
        col_nombre: str = 'Nombre',
        col_latitud: str = 'Latitud',
        col_longitud: str = 'Longitud'
    ) -> Tuple[np.ndarray, List[str]]:
        """
        Carga coordenadas desde un archivo Excel.

        Args:
            archivo: Ruta al archivo Excel
            col_nombre: Nombre de la columna con nombres
            col_latitud: Nombre de la columna con latitudes
            col_longitud: Nombre de la columna con longitudes

        Returns:
            Tupla (coordenadas, nombres)
        """
        print(f"📂 Cargando dataset: {archivo}")

        try:
            self.df = pd.read_excel(archivo)
            print(f"✓ Archivo cargado: {len(self.df)} registros")
        except Exception as e:
            print(f"❌ Error al cargar archivo: {e}")
            raise

        # Verificar columnas
        columnas_necesarias = [col_nombre, col_latitud, col_longitud]
        columnas_faltantes = [col for col in columnas_necesarias if col not in self.df.columns]

        if columnas_faltantes:
            print(f"❌ Columnas faltantes: {columnas_faltantes}")
            print(f"   Columnas disponibles: {self.df.columns.tolist()}")
            raise ValueError(f"Columnas faltantes: {columnas_faltantes}")

        # Limpiar datos
        print("🧹 Limpiando datos...")
        df_limpio = self.df.copy()

        # Eliminar filas con valores nulos
        df_limpio = df_limpio.dropna(subset=[col_nombre, col_latitud, col_longitud])

        # Convertir coordenadas a numérico
        df_limpio[col_latitud] = pd.to_numeric(df_limpio[col_latitud], errors='coerce')
        df_limpio[col_longitud] = pd.to_numeric(df_limpio[col_longitud], errors='coerce')

        # Eliminar filas con coordenadas inválidas
        df_limpio = df_limpio.dropna(subset=[col_latitud, col_longitud])

        # Validar rangos
        df_limpio = df_limpio[
            (df_limpio[col_latitud] >= -90) & (df_limpio[col_latitud] <= 90) &
            (df_limpio[col_longitud] >= -180) & (df_limpio[col_longitud] <= 180)
        ]

        print(f"✓ Datos limpios: {len(df_limpio)} registros válidos")

        if len(df_limpio) == 0:
            raise ValueError("No hay datos válidos después de la limpieza")

        # Extraer coordenadas y nombres
        self.coordenadas = df_limpio[[col_latitud, col_longitud]].values
        self.nombres = df_limpio[col_nombre].astype(str).tolist()

        return self.coordenadas, self.nombres

    def crear_dataset_muestra(
        self,
        n_puntos: int = 20,
        lat_centro: float = -12.0464,
        lon_centro: float = -77.0428,
        radio: float = 0.5
    ) -> Tuple[np.ndarray, List[str]]:
        """
        Crea un dataset de muestra aleatorio.

        Args:
            n_puntos: Número de puntos a generar
            lat_centro: Latitud del centro
            lon_centro: Longitud del centro
            radio: Radio en grados para dispersión

        Returns:
            Tupla (coordenadas, nombres)
        """
        print(f"🎲 Generando dataset de muestra: {n_puntos} puntos")

        np.random.seed(42)

        # Generar coordenadas aleatorias alrededor del centro
        latitudes = np.random.uniform(
            lat_centro - radio,
            lat_centro + radio,
            n_puntos
        )

        longitudes = np.random.uniform(
            lon_centro - radio,
            lon_centro + radio,
            n_puntos
        )

        self.coordenadas = np.column_stack([latitudes, longitudes])
        self.nombres = [f"Punto_{i+1}" for i in range(n_puntos)]

        print(f"✓ Dataset generado: {len(self.nombres)} puntos")

        return self.coordenadas, self.nombres

    def limitar_puntos(self, max_puntos: int) -> Tuple[np.ndarray, List[str]]:
        """
        Limita el dataset a un número máximo de puntos.

        Args:
            max_puntos: Número máximo de puntos

        Returns:
            Tupla (coordenadas, nombres) limitados
        """
        if self.coordenadas is None or len(self.coordenadas) <= max_puntos:
            return self.coordenadas, self.nombres

        print(f"✂️ Limitando dataset de {len(self.coordenadas)} a {max_puntos} puntos")

        # Tomar los primeros max_puntos
        self.coordenadas = self.coordenadas[:max_puntos]
        self.nombres = self.nombres[:max_puntos]

        return self.coordenadas, self.nombres

    def calcular_matriz_distancias(self, usar_geodesica: bool = False) -> np.ndarray:
        """
        Calcula la matriz de distancias entre todos los puntos.

        Args:
            usar_geodesica: Si True, usa distancia geodésica; si False, euclidiana

        Returns:
            Matriz de distancias (N, N)
        """
        if self.coordenadas is None:
            raise ValueError("No hay coordenadas cargadas")

        n = len(self.coordenadas)
        matriz = np.zeros((n, n))

        print(f"📏 Calculando matriz de distancias ({n}x{n})...")

        for i in range(n):
            for j in range(i + 1, n):
                if usar_geodesica:
                    # Distancia geodésica en kilómetros
                    dist = geodesic(
                        self.coordenadas[i],
                        self.coordenadas[j]
                    ).kilometers
                else:
                    # Distancia euclidiana
                    dist = np.linalg.norm(
                        self.coordenadas[i] - self.coordenadas[j]
                    )

                matriz[i, j] = dist
                matriz[j, i] = dist

        print(f"✓ Matriz calculada")

        return matriz

    def obtener_estadisticas(self) -> dict:
        """
        Obtiene estadísticas del dataset.

        Returns:
            Diccionario con estadísticas
        """
        if self.coordenadas is None:
            return {}

        return {
            'n_puntos': len(self.coordenadas),
            'lat_min': float(self.coordenadas[:, 0].min()),
            'lat_max': float(self.coordenadas[:, 0].max()),
            'lon_min': float(self.coordenadas[:, 1].min()),
            'lon_max': float(self.coordenadas[:, 1].max()),
            'lat_centro': float(self.coordenadas[:, 0].mean()),
            'lon_centro': float(self.coordenadas[:, 1].mean()),
            'nombres': self.nombres
        }

    def exportar_a_excel(self, archivo: str = 'dataset_procesado.xlsx'):
        """
        Exporta el dataset procesado a Excel.

        Args:
            archivo: Nombre del archivo de salida
        """
        if self.coordenadas is None:
            print("⚠️ No hay datos para exportar")
            return

        df_export = pd.DataFrame({
            'Nombre': self.nombres,
            'Latitud': self.coordenadas[:, 0],
            'Longitud': self.coordenadas[:, 1]
        })

        df_export.to_excel(archivo, index=False)
        print(f"✓ Dataset exportado a: {archivo}")

