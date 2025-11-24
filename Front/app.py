import os
import sys
import json
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename

# Add Hito-2 to python path to import existing modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Hito-2')))

from dataset_processor import DatasetProcessor
from sistema_optimizacion import OptimizadorRutasHibrido

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/optimize', methods=['POST'])
def optimize():
    try:
        coordenadas = None
        nombres = None
        processor = DatasetProcessor()

        # Check if using CSV database
        if request.form.get('use_csv') == 'true':
            csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Hito-2', '1_Dataset_Intervenciones_PVD_30062025.csv'))
            n_points = int(request.form.get('n_points', 50))

            if os.path.exists(csv_path):
                coordenadas, nombres = processor.cargar_desde_csv_intervenciones(csv_path, max_puntos=n_points)
            else:
                return jsonify({'error': 'CSV de intervenciones no encontrado'}), 400

        # Check if file was uploaded
        elif 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # Detect file type
                if filename.lower().endswith('.csv'):
                    coordenadas, nombres = processor.cargar_desde_csv_intervenciones(filepath)
                else:
                    coordenadas, nombres = processor.cargar_desde_excel(filepath)

                # Limit points for performance if needed
                max_puntos = int(request.form.get('max_points', 100))
                if len(coordenadas) > max_puntos:
                    coordenadas, nombres = processor.limitar_puntos(max_puntos)

        # Check if using random data
        elif request.form.get('use_random') == 'true':
            n_points = int(request.form.get('n_points', 20))
            coordenadas, nombres = processor.crear_dataset_muestra(n_puntos=n_points)
            
        if coordenadas is None:
            return jsonify({'error': 'No se proporcionaron datos válidos'}), 400

        # Run optimization
        n_clusters = int(request.form.get('n_clusters', 5))
        metodo_tsp = request.form.get('metodo_tsp', 'auto')
        optimizador = OptimizadorRutasHibrido(n_clusters=n_clusters)
        resultados = optimizador.optimizar(coordenadas, nombres, metodo_tsp=metodo_tsp)

        # Prepare response for frontend
        ruta_global_coords = []
        ruta_global_nombres = []
        
        # The 'ruta_global' in resultados contains indices of the original coordinates array
        for idx in resultados['ruta_global']:
            ruta_global_coords.append(coordenadas[idx].tolist())
            ruta_global_nombres.append(nombres[idx])
            
        # Also return cluster info for coloring
        clusters_info = []
        colores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8',
                   '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B739', '#52B788']

        for i, cluster in enumerate(resultados['clusters']):
            cluster_coords = [coordenadas[idx].tolist() for idx in cluster['ruta_global']]
            cluster_nombres = [nombres[idx] for idx in cluster['ruta_global']]
            clusters_info.append({
                'id': cluster['cluster_id'],
                'coords': cluster_coords,
                'nombres': cluster_nombres,
                'color': colores[i % len(colores)],
                'n_puntos': cluster['n_puntos'],
                'distancia': cluster['distancia'],
                'metodo': cluster.get('metodo', 'auto')
            })

        return jsonify({
            'status': 'success',
            'route_coords': ruta_global_coords,
            'route_names': ruta_global_nombres,
            'clusters': clusters_info,
            'stats': {
                'total_distance': resultados['distancia_total'],
                'distance_within_clusters': resultados['distancia_dentro_clusters'],
                'distance_between_clusters': resultados['distancia_entre_clusters'],
                'execution_time': resultados['estadisticas']['tiempo_total'],
                'clustering_time': resultados['estadisticas']['tiempo_clustering'],
                'tsp_time': resultados['estadisticas']['tiempo_tsp'],
                'n_points': resultados['n_puntos_total'],
                'n_clusters': resultados['n_clusters']
            }
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
