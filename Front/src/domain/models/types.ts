export interface Node {
    id: string;
    lat: number;
    lon: number;
    name: string;
}

export interface Cluster {
    id: number;
    coords: number[][];
    names: string[];
    color: string;
    n_puntos: number;
    centroid?: number[];
}

export interface RouteStats {
    total_distance: number;
    execution_time: number;
    clustering_time: number;
    tsp_time: number;
    n_points: number;
    n_clusters: number;
    warning?: string;
}

export interface OptimizationResult {
    status: string;
    route_coords: number[][];
    route_names: string[];
    clusters: Cluster[];
    stats: RouteStats;
}
