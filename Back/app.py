from flask import Flask, jsonify, send_file
import os
from main import main as ejecutar_optimizacion

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "mensaje": "API de Optimización de Rutas activa",
        "endpoints": {
            "/": "Este mensaje",
            "/optimizar": "Ejecuta la optimización"
        }
    })

@app.route('/optimizar')
def optimizar():
    try:
        ejecutar_optimizacion()
        return jsonify({
            "status": "success",
            "mensaje": "Optimización completada"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
