from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional, List
import numpy as np
import time

from domain.services.tsp_service import TSPService
from domain.services.clustering_service import ClusteringService
from infrastructure.persistence.csv_repository import CSVRepository
from application.dtos.request_dtos import OptimizeRequest, ManualPoint
from application.dtos.response_dtos import OptimizeResponse, ClusterResponse, StatsResponse

router = APIRouter()

@router.post("/optimize", response_model=OptimizeResponse)
async def optimize(
    file: Optional[UploadFile] = File(None),
    n_clusters: int = Form(5),
    method: str = Form('auto'),
    use_csv: bool = Form(False),
    date_filter: Optional[str] = Form(None),
    manual_points_json: Optional[str] = Form(None), # Receive as JSON string if sent via Form
    max_points: int = Form(50)
):
    try:
        start_time = time.time()
        
        # Load Data
        repo = CSVRepository()
        coords = None
        names = None

        # Handle Manual Points
        if manual_points_json:
            import json
            points_data = json.loads(manual_points_json)
            coords_list = [[p['lat'], p['lng']] for p in points_data]
            names = [p.get('name', f'Point {i}') for i, p in enumerate(points_data)]
            coords = np.array(coords_list)
        
        # Handle CSV
        elif use_csv:
            coords, names = repo.load_data(date_filter=date_filter, max_points=max_points)
            
        # Handle File Upload
        elif file:
            content = await file.read()
            if file.filename.endswith('.csv'):
                # For now, reuse CSV loader logic if possible or implement specific CSV upload
                # But repo.load_data loads from the specific project CSV. 
                # If uploading a NEW CSV, we need logic.
                # For simplicity, let's assume Excel upload as per original app
                pass
            else:
                coords, names = repo.load_from_excel(content, max_points=max_points)
        
        # Handle Random/Default
        if coords is None:
             # Fallback to random if nothing else
             # Or raise error
             pass

             # Generate random sample in MACRO REGION (Trujillo to Nazca)
             # User requested "5x bigger" again.
             # Bounding Box:
             # Lat: -15.00 (Nazca/Marcona) to -8.00 (Trujillo)
             # Lon: -79.50 (Ocean limit) to -74.00 (Ayacucho/Huancayo)
             
             count = max_points if max_points else 20
             np.random.seed(int(time.time()))
             
             coords_list = []
             names = []
             
             while len(coords_list) < count:
                 # Generate batch in MACRO REGIONAL bounding box
                 batch_size = count * 2
                 lats = np.random.uniform(-15.00, -8.00, batch_size)
                 lons = np.random.uniform(-79.50, -74.00, batch_size)
                 
                 for lat, lon in zip(lats, lons):
                     # General Coastline Equation for Central-South Peru
                     # Fits Trujillo (-8, -79) to Lima (-12, -77) to Ica (-14, -76)
                     # Slope approx: -0.5
                     # Equation: Lon > -0.5 * Lat - 83.2
                     
                     if lon > (-0.5 * lat - 83.2):
                         coords_list.append([lat, lon])
                         if len(coords_list) >= count:
                             break
             
             coords = np.array(coords_list)
             names = [f"Punto_MacroRegion_{i+1}" for i in range(count)]

        # Clustering
        # Ensure n_clusters is not greater than n_points
        n_points = len(coords)
        if n_clusters > n_points:
            n_clusters = max(1, n_points)
            
        clustering_start = time.time()
        cluster_service = ClusteringService(n_clusters=n_clusters)
        clusters_data = cluster_service.get_clusters(coords, names)
        clustering_time = time.time() - clustering_start

        # TSP per cluster
        tsp_start = time.time()
        tsp_service = TSPService()
        
        final_route_indices = []
        total_distance = 0
        
        # Sort clusters (nearest neighbor of centroids)
        # For now, just iterate 0..k
        
        processed_clusters = []
        colores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8',
                   '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B739', '#52B788']

        for i, cluster in enumerate(clusters_data):
            cluster_coords = np.array(cluster['coords'])
            # Solve TSP for this cluster
            route_local_indices, dist, _ = tsp_service.solve(cluster_coords, method)
            
            # Map back to global indices
            global_indices = [cluster['original_indices'][idx] for idx in route_local_indices]
            final_route_indices.extend(global_indices)
            
            processed_clusters.append(ClusterResponse(
                id=cluster['id'],
                coords=cluster['coords'],
                names=cluster['names'],
                color=colores[i % len(colores)],
                n_puntos=len(cluster['coords']),
                centroid=cluster['centroid']
            ))

        # Recalculate Total Distance of the FINAL route to include inter-cluster travel
        full_dist_matrix = tsp_service._precompute_distance_matrix(coords)
        total_distance = tsp_service.calculate_total_distance(full_dist_matrix, final_route_indices)
        
        tsp_time = time.time() - tsp_start

        # Build response
        route_coords = coords[final_route_indices].tolist()
        route_names = [names[i] for i in final_route_indices]
        
        return OptimizeResponse(
            status="success",
            route_coords=route_coords,
            route_names=route_names,
            clusters=processed_clusters,
            stats=StatsResponse(
                total_distance=total_distance,
                execution_time=time.time() - start_time,
                clustering_time=clustering_time,
                tsp_time=tsp_time,
                n_points=len(coords),
                n_clusters=n_clusters
            )
        )

    except ValueError as ve:
        # Catch specific value errors (like no data found) and return 400
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        import traceback
        traceback.print_exc() # Print stack trace to console for debugging
        raise HTTPException(status_code=500, detail=str(e))
