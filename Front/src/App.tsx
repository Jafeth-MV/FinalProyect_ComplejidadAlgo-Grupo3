import { useState, useEffect } from 'react';
import { MapView } from './components/MapView';
import { optimizeRoute } from './infrastructure/api/client';
import type { OptimizationResult } from './domain/models/types';
import { Map as MapIcon, Calendar, Upload, MousePointer, Shuffle, FileSpreadsheet } from 'lucide-react';

function App() {
  const [result, setResult] = useState<OptimizationResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [manualPoints, setManualPoints] = useState<{ lat: number; lng: number; name: string }[]>([]);
  const [mode, setMode] = useState<'csv' | 'upload' | 'manual' | 'random'>('csv');
  const [nPoints, setNPoints] = useState(50);
  const [nClusters, setNClusters] = useState(5);
  const [dateFilter, setDateFilter] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [algorithm, setAlgorithm] = useState('auto');

  // Clear state when switching modes
  useEffect(() => {
    setManualPoints([]);
    setResult(null);
    setFile(null);
    setDateFilter('');
  }, [mode]);

  const handleMapClick = (lat: number, lng: number) => {
    if (mode === 'manual') {
      setManualPoints([...manualPoints, { lat, lng, name: `Punto ${manualPoints.length + 1}` }]);
    }
  };

  const handleOptimize = async () => {
    setLoading(true);
    try {
      // For random mode, we don't send file, csv flag, or manual points. 
      // The backend fallback will handle it.
      setResult(null); // Clear previous results

      const res = await optimizeRoute({
        n_clusters: nClusters,
        method: algorithm,
        use_csv: mode === 'csv',
        file: mode === 'upload' ? (file || undefined) : undefined,
        date_filter: mode === 'csv' ? (dateFilter || undefined) : undefined,
        manual_points: mode === 'manual' ? manualPoints : undefined,
        max_points: nPoints
      });
      setResult(res);
    } catch (error: any) {
      console.error(error);
      const msg = error.response?.data?.detail || 'Error al optimizar ruta';
      alert(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-[#1a1d21] text-white font-sans">
      {/* Sidebar */}
      <div className="w-[350px] bg-[#111315] p-6 flex flex-col gap-6 shadow-2xl z-20 border-r border-gray-800 overflow-y-auto">

        {/* Header */}
        <div className="flex items-center gap-3 mb-2">
          <div className="bg-blue-600 p-2 rounded-lg">
            <MapIcon className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight">RutaFix</h1>
            <p className="text-xs text-gray-400">Sistema de Optimización</p>
          </div>
        </div>

        {/* Mode Selection - Tabs */}
        <div className="flex flex-col gap-2">
          <label className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Modo de Datos</label>
          <div className="grid grid-cols-2 gap-2">
            <button
              onClick={() => setMode('csv')}
              className={`flex items-center justify-center gap-2 p-3 text-xs font-medium rounded-lg transition-all ${mode === 'csv' ? 'bg-blue-600 text-white shadow-lg shadow-blue-900/20' : 'bg-[#1c1f24] text-gray-400 hover:bg-[#25282e] hover:text-gray-200'}`}
            >
              <Calendar className="w-3 h-3" /> Base CSV
            </button>
            <button
              onClick={() => setMode('upload')}
              className={`flex items-center justify-center gap-2 p-3 text-xs font-medium rounded-lg transition-all ${mode === 'upload' ? 'bg-blue-600 text-white shadow-lg shadow-blue-900/20' : 'bg-[#1c1f24] text-gray-400 hover:bg-[#25282e] hover:text-gray-200'}`}
            >
              <Upload className="w-3 h-3" /> Subir Excel
            </button>
            <button
              onClick={() => setMode('manual')}
              className={`flex items-center justify-center gap-2 p-3 text-xs font-medium rounded-lg transition-all ${mode === 'manual' ? 'bg-blue-600 text-white shadow-lg shadow-blue-900/20' : 'bg-[#1c1f24] text-gray-400 hover:bg-[#25282e] hover:text-gray-200'}`}
            >
              <MousePointer className="w-3 h-3" /> Manual
            </button>
            <button
              onClick={() => setMode('random')}
              className={`flex items-center justify-center gap-2 p-3 text-xs font-medium rounded-lg transition-all ${mode === 'random' ? 'bg-blue-600 text-white shadow-lg shadow-blue-900/20' : 'bg-[#1c1f24] text-gray-400 hover:bg-[#25282e] hover:text-gray-200'}`}
            >
              <Shuffle className="w-3 h-3" /> Aleatorio
            </button>
          </div>
        </div>

        {/* Controls Panel */}
        <div className="flex flex-col gap-5 bg-[#16181b] p-4 rounded-xl border border-gray-800/50">

          {/* CSV Mode Controls */}
          {mode === 'csv' && (
            <div className="space-y-3">
              <div className="flex items-center gap-2 text-blue-400 mb-1">
                <FileSpreadsheet className="w-4 h-4" />
                <span className="text-sm font-medium">Dataset de Intervenciones</span>
              </div>

              <div className="space-y-1">
                <label className="text-xs text-gray-500">Filtrar por Fecha de Corte</label>
                <div className="relative">
                  <select
                    value={dateFilter || ''}
                    onChange={(e) => setDateFilter(e.target.value)}
                    className="w-full bg-[#1c1f24] border border-gray-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500 transition-colors appearance-none"
                  >
                    <option value="">-- Seleccionar Fecha --</option>
                    <option value="20240630">30 de Junio 2024</option>
                    <option value="20241231">31 de Diciembre 2024</option>
                    <option value="20250630">30 de Junio 2025 (Proyección)</option>
                  </select>
                  <Calendar className="absolute right-3 top-2.5 w-4 h-4 text-gray-500 pointer-events-none" />
                </div>
                <p className="text-[10px] text-gray-500 mt-1">
                  * Fechas de Corte Semestral del MTC.
                </p>
              </div>
            </div>
          )}

          {/* Upload Mode Controls */}
          {mode === 'upload' && (
            <div className="relative group">
              <input
                type="file"
                accept=".xlsx,.xls,.csv"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
              />
              <div className={`border-2 border-dashed rounded-lg p-6 text-center transition-all ${file ? 'border-blue-500 bg-blue-500/10' : 'border-gray-700 hover:border-gray-500 hover:bg-gray-800'}`}>
                <Upload className={`w-8 h-8 mx-auto mb-2 ${file ? 'text-blue-400' : 'text-gray-500'}`} />
                <p className="text-sm font-medium text-gray-300 truncate px-2">
                  {file ? file.name : 'Click o arrastra archivo'}
                </p>
                <p className="text-xs text-gray-500 mt-1">Soporta .xlsx, .csv</p>

                {/* Format Guide */}
                <div className="mt-4 flex flex-col items-center gap-2 bg-[#16181b] p-2 rounded border border-gray-800/50">
                  <div className="flex items-center gap-2 text-yellow-500/80">
                    <FileSpreadsheet className="w-4 h-4" />
                    <span className="text-xs font-mono">ejemplo.xlsx</span>
                  </div>
                  <p className="text-[10px] text-gray-400">
                    Formato requerido: <span className="text-gray-300 font-medium">Nombre, Latitud, Longitud</span>
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Manual Mode Controls */}
          {mode === 'manual' && (
            <div className="bg-blue-900/20 p-4 rounded-lg border border-blue-500/20">
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium text-blue-200">Puntos Marcados</span>
                <span className="bg-blue-600 text-xs px-2 py-0.5 rounded-full">{manualPoints.length}</span>
              </div>
              <p className="text-xs text-gray-400 mb-3">Haz clic en el mapa para agregar destinos.</p>

              {manualPoints.length > 0 && (
                <button
                  onClick={() => setManualPoints([])}
                  className="text-xs text-red-400 hover:text-red-300 hover:underline w-full text-right"
                >
                  Limpiar todos
                </button>
              )}
            </div>
          )}

          {/* Random Mode Controls */}
          {mode === 'random' && (
            <div className="bg-purple-900/20 p-4 rounded-lg border border-purple-500/20">
              <div className="flex items-center gap-2 mb-2">
                <Shuffle className="w-4 h-4 text-purple-400" />
                <span className="text-sm font-medium text-purple-200">Generación Aleatoria</span>
              </div>
              <p className="text-xs text-gray-400">
                Se generarán puntos aleatorios alrededor de Lima para demostración.
              </p>
            </div>
          )}

          {/* Common Sliders */}
          <div className="space-y-4 pt-2 border-t border-gray-800">
            <div className="space-y-2">
              <div className="flex justify-between text-xs">
                <span className="text-gray-400">Algoritmo</span>
              </div>
              <select
                value={algorithm}
                onChange={(e) => setAlgorithm(e.target.value)}
                className="w-full bg-[#1c1f24] border border-gray-700 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-blue-500 transition-colors"
              >
                <option value="auto">Automático (Recomendado)</option>
                <option value="nearest_neighbor">Vecino Más Cercano (Rápido)</option>
                <option value="dijkstra">Dijkstra (Ruta Óptima)</option>
                <option value="kruskal">Kruskal (MST)</option>
                <option value="k_means">K-Means (Clustering)</option>
              </select>
            </div>

            <div className="space-y-2">
              <div className="flex justify-between text-xs">
                <span className="text-gray-400">Cantidad de Puntos</span>
                <span className="text-blue-400 font-mono">{nPoints}</span>
              </div>
              <input
                type="range"
                min="10"
                max="200"
                value={nPoints}
                onChange={(e) => setNPoints(Number(e.target.value))}
                className="w-full h-1 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-blue-500"
              />
            </div>

            <div className="space-y-2">
              <div className="flex justify-between text-xs">
                <span className="text-gray-400">Número de Clusters</span>
                <span className="text-blue-400 font-mono">{nClusters}</span>
              </div>
              <input
                type="range"
                min="1"
                max="10"
                value={nClusters}
                onChange={(e) => setNClusters(Number(e.target.value))}
                className="w-full h-1 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-blue-500"
              />
            </div>

            <button
              onClick={handleOptimize}
              disabled={loading}
              className={`w-full py-3 rounded-lg font-bold text-sm transition-all transform active:scale-95 shadow-lg ${loading ? 'bg-gray-700 text-gray-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-500 text-white shadow-blue-900/30'}`}
            >
              {loading ? 'Procesando...' : 'Optimizar Ruta'}
            </button>
          </div>
        </div>

        {/* Results Panel */}
        {result && (
          <div className="bg-[#16181b] p-4 rounded-xl border border-gray-800/50 space-y-3">
            <div className="flex items-center gap-2 mb-2">
              <div className="bg-green-500/20 p-1.5 rounded-md">
                <FileSpreadsheet className="w-4 h-4 text-green-400" />
              </div>
              <h3 className="font-bold text-sm text-gray-200">Resultados</h3>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div className="bg-[#1c1f24] p-3 rounded-lg border border-gray-800">
                <p className="text-[10px] text-gray-500 uppercase tracking-wider font-semibold">Distancia Total</p>
                <p className="text-lg font-bold text-green-400">
                  {result.stats.total_distance.toFixed(2)} <span className="text-xs text-gray-500">km</span>
                </p>
              </div>
              <div className="bg-[#1c1f24] p-3 rounded-lg border border-gray-800">
                <p className="text-[10px] text-gray-500 uppercase tracking-wider font-semibold">Tiempo Proceso</p>
                <p className="text-lg font-bold text-blue-400">
                  {result.stats.execution_time.toFixed(3)} <span className="text-xs text-gray-500">s</span>
                </p>
              </div>
            </div>

            <div className="bg-[#1c1f24] p-3 rounded-lg border border-gray-800 flex flex-col flex-1 min-h-0">
              <p className="text-[10px] text-gray-500 uppercase tracking-wider font-semibold mb-2">Ruta Optimizada</p>
              <div className="text-xs text-gray-400 max-h-48 overflow-y-auto space-y-1 custom-scrollbar pr-1">
                {result.route_names.map((name, idx) => (
                  <div key={idx} className="flex gap-2 items-center hover:bg-gray-800/50 p-1 rounded">
                    <span className="text-gray-600 font-mono w-5 text-right">{idx + 1}.</span>
                    <span className="truncate">{name}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Map Area */}
      <div className="flex-1 relative">
        <MapView
          routeCoords={result?.route_coords || []}
          clusters={result?.clusters || []}
          manualPoints={manualPoints}
          onMapClick={handleMapClick}
          isManualMode={mode === 'manual'}
        />

        {/* Loading Overlay */}
        {loading && (
          <div className="absolute inset-0 bg-black/60 backdrop-blur-sm z-[1000] flex items-center justify-center">
            <div className="bg-[#16181b] p-6 rounded-2xl shadow-2xl border border-gray-800 flex flex-col items-center gap-4">
              <div className="relative w-12 h-12">
                <div className="absolute inset-0 border-4 border-blue-500/30 rounded-full"></div>
                <div className="absolute inset-0 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
              </div>
              <div className="text-center">
                <p className="text-white font-medium">Optimizando Ruta</p>
                <p className="text-xs text-gray-400 mt-1">Calculando mejor trayecto...</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
