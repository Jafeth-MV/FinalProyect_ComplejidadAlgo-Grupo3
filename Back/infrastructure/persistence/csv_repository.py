import pandas as pd
import numpy as np
from typing import Tuple, List, Optional
from datetime import datetime
import os

class CSVRepository:
    _df_cache = None

    def __init__(self, csv_path: str = '1_Dataset_Intervenciones_PVD_30062025.csv'):
        # Adjust path to be relative to the Back directory if needed, or absolute
        # Assuming the CSV is in the root of Back
        self.csv_path = csv_path
        self.coords_departamentos = {
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

    def load_data(self, date_filter: Optional[str] = None, max_points: int = 50) -> Tuple[np.ndarray, List[str]]:
        if CSVRepository._df_cache is not None:
            df = CSVRepository._df_cache.copy()
        else:
            if not os.path.exists(self.csv_path):
                # Try looking one level up or in current dir
                if os.path.exists(os.path.join('..', self.csv_path)):
                    self.csv_path = os.path.join('..', self.csv_path)
                elif os.path.exists(os.path.join('Back', self.csv_path)):
                    self.csv_path = os.path.join('Back', self.csv_path)
                else:
                     # Fallback to absolute path if possible or raise error
                     pass

            df = None
            cols_to_use = ['CODIGO_RUTA', 'DEPARTAMENTO', 'PROVINCIA', 'FECHA_CORTE']
            
            for encoding in ['latin1', 'iso-8859-1', 'cp1252']:
                try:
                    # Read all rows first to filter
                    df = pd.read_csv(self.csv_path, sep=';', encoding=encoding, usecols=cols_to_use, dtype=str)
                    break
                except Exception:
                    continue
            
            if df is None:
                raise ValueError("Could not load CSV file")
            
            # Pre-processing for speed
            # Ensure FECHA_CORTE is string and strip whitespace
            df['FECHA_CORTE'] = df['FECHA_CORTE'].astype(str).str.strip()
            # Sort by FECHA_CORTE for faster access
            df.sort_values('FECHA_CORTE', inplace=True)
            
            CSVRepository._df_cache = df.copy()

        # Filter by date if provided
        # Use a fresh copy from cache to avoid chaining filters on the same object reference issues (though unlikely with pandas copy)
        # But to be safe and fast:
        df_working = CSVRepository._df_cache
        
        if date_filter:
            date_str = str(date_filter).replace('-', '')
            # Vectorized boolean indexing is fast
            df_working = df_working[df_working['FECHA_CORTE'] == date_str]
            
            if len(df_working) == 0:
                raise ValueError(f"No data found for date {date_filter}")

        # Unique routes
        # head(max_points) optimization: take only what we need immediately
        rutas_unicas = df_working.drop_duplicates(subset=['CODIGO_RUTA']).head(max_points)
        
        coordenadas_list = []
        nombres_list = []
        
        np.random.seed(42)

        for _, row in rutas_unicas.iterrows():
            try:
                codigo_ruta = str(row['CODIGO_RUTA'])
                dept_raw = str(row['DEPARTAMENTO'])
                provincia = str(row.get('PROVINCIA', 'Desconocida'))

                dept = dept_raw.strip().upper()
                if '-' in dept:
                    dept = dept.split('-')[0].strip()

                if dept in self.coords_departamentos:
                    base_lat, base_lon = self.coords_departamentos[dept]
                    lat = base_lat + np.random.uniform(-0.3, 0.3)
                    lon = base_lon + np.random.uniform(-0.3, 0.3)
                    
                    coordenadas_list.append([lat, lon])
                    nombres_list.append(f"{codigo_ruta}_{provincia[:15]}")
            except Exception:
                continue
                
        if not coordenadas_list:
             # Fallback if filtering resulted in empty but we need data for demo?
             # Or just raise error
             if date_filter:
                 raise ValueError(f"No valid coordinates found for date {date_filter}")
             raise ValueError("No valid coordinates found in CSV")

        return np.array(coordenadas_list), nombres_list

    def load_from_excel(self, file_content: bytes, max_points: int = 100) -> Tuple[np.ndarray, List[str]]:
        # This would require saving bytes to temp file or using BytesIO
        import io
        df = pd.read_excel(io.BytesIO(file_content))
        
        # Basic validation similar to original
        required = ['Latitud', 'Longitud', 'Nombre']
        if not all(col in df.columns for col in required):
             # Try to be flexible?
             pass
        
        df = df.dropna(subset=['Latitud', 'Longitud'])
        if len(df) > max_points:
            df = df.head(max_points)
            
        coords = df[['Latitud', 'Longitud']].values
        names = df['Nombre'].astype(str).tolist()
        return coords, names
