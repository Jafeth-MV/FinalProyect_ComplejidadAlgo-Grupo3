"""
Script de prueba rápida para verificar que el sistema funciona con el CSV
"""

import sys
import os

# Add Hito-2 to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Hito-2'))

from dataset_processor import DatasetProcessor
from sistema_optimizacion import OptimizadorRutasHibrido

def test_csv_loading():
    """Prueba la carga del CSV"""
    print("=" * 70)
    print("🧪 PRUEBA DE CARGA DEL CSV")
    print("=" * 70)

    csv_path = os.path.join(os.path.dirname(__file__), '..', 'Hito-2', '1_Dataset_Intervenciones_PVD_30062025.csv')

    if not os.path.exists(csv_path):
        print("❌ El archivo CSV no existe en la ubicación esperada")
        return False

    processor = DatasetProcessor()

    try:
        coordenadas, nombres = processor.cargar_desde_csv_intervenciones(csv_path, max_puntos=25)

        print(f"✅ CSV cargado correctamente")
        print(f"   Coordenadas generadas: {len(coordenadas)}")
        print(f"   Primeros 5 nombres:")
        for i, nombre in enumerate(nombres[:5], 1):
            print(f"      {i}. {nombre}")

        return True

    except Exception as e:
        print(f"❌ Error al cargar CSV: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_optimization():
    """Prueba la optimización completa"""
    print("\n" + "=" * 70)
    print("🧪 PRUEBA DE OPTIMIZACIÓN")
    print("=" * 70)

    csv_path = os.path.join(os.path.dirname(__file__), '..', 'Hito-2', '1_Dataset_Intervenciones_PVD_30062025.csv')

    processor = DatasetProcessor()

    try:
        coordenadas, nombres = processor.cargar_desde_csv_intervenciones(csv_path, max_puntos=15)

        print(f"✅ Datos cargados: {len(coordenadas)} puntos")

        optimizador = OptimizadorRutasHibrido(n_clusters=3)
        resultados = optimizador.optimizar(coordenadas, nombres, metodo_tsp='auto')

        print(f"✅ Optimización completada")
        print(f"   Distancia total: {resultados['distancia_total']:.4f} km")
        print(f"   Clusters: {resultados['n_clusters']}")
        print(f"   Tiempo total: {resultados['estadisticas']['tiempo_total']:.2f}s")

        print(f"\n📍 Primeros 5 puntos de la ruta:")
        ruta_nombres = optimizador.obtener_ruta_nombres()
        for i, nombre in enumerate(ruta_nombres[:5], 1):
            print(f"      {i}. {nombre}")

        return True

    except Exception as e:
        print(f"❌ Error en optimización: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Ejecuta todas las pruebas"""
    print("\n🚀 INICIANDO PRUEBAS DEL SISTEMA\n")

    results = []

    # Test 1: Carga del CSV
    results.append(("Carga del CSV", test_csv_loading()))

    # Test 2: Optimización
    results.append(("Optimización", test_optimization()))

    # Resumen
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 70)

    for test_name, passed in results:
        status = "✅ PASÓ" if passed else "❌ FALLÓ"
        print(f"{test_name}: {status}")

    all_passed = all(result[1] for result in results)

    print("\n" + "=" * 70)
    if all_passed:
        print("🎉 TODAS LAS PRUEBAS PASARON")
    else:
        print("⚠️ ALGUNAS PRUEBAS FALLARON")
    print("=" * 70)

    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

