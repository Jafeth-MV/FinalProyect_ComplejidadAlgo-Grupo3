from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class ClusterResponse(BaseModel):
    id: int
    coords: List[List[float]]
    names: List[str]
    color: str
    n_puntos: int
    centroid: Optional[List[float]]

class StatsResponse(BaseModel):
    total_distance: float
    execution_time: float
    clustering_time: float
    tsp_time: float
    n_points: int
    n_clusters: int
    warning: Optional[str] = None

class OptimizeResponse(BaseModel):
    status: str
    route_coords: List[List[float]]
    route_names: List[str]
    clusters: List[ClusterResponse]
    stats: StatsResponse
