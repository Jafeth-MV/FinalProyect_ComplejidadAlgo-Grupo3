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
        
        # Check if file was uploaded
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                processor = DatasetProcessor()
                # We need to modify dataset_processor to handle the file path correctly or use the one we just saved
                coordenadas, nombres = processor.cargar_desde_excel(filepath)
                
                # Limit points for performance if needed (optional, maybe parameterize)
                if len(coordenadas) > 100:
                    coordenadas, nombres = processor.limitar_puntos(100)
        
        # Check if using random data
        elif request.form.get('use_random') == 'true':
            n_points = int(request.form.get('n_points', 20))
            processor = DatasetProcessor()
            coordenadas, nombres = processor.crear_dataset_muestra(n_puntos=n_points)
            
        if coordenadas is None:
            return jsonify({'error': 'No se proporcionaron datos válidos'}), 400

        # Run optimization
        n_clusters = int(request.form.get('n_clusters', 5))
        optimizador = OptimizadorRutasHibrido(n_clusters=n_clusters)
        resultados = optimizador.optimizar(coordenadas, nombres)
        
        # Prepare response for frontend
        # We need the ordered list of coordinates to draw the route
        ruta_global_coords = []
        ruta_global_nombres = []
        
        # The 'ruta_global' in resultados contains indices of the original coordinates array
        for idx in resultados['ruta_global']:
            ruta_global_coords.append(coordenadas[idx].tolist())
            ruta_global_nombres.append(nombres[idx])
            
        # Also return cluster info for coloring
        clusters_info = []
        for cluster in resultados['clusters']:
            cluster_coords = [coordenadas[idx].tolist() for idx in cluster['ruta_global']]
            clusters_info.append({
                'id': cluster['cluster_id'],
                'coords': cluster_coords,
                'color': 'auto' # Frontend will assign colors
            })

        return jsonify({
            'status': 'success',
            'route_coords': ruta_global_coords,
            'route_names': ruta_global_nombres,
            'clusters': clusters_info,
            'stats': {
                'total_distance': resultados['distancia_total'],
                'execution_time': resultados['estadisticas']['tiempo_total']
            }
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
