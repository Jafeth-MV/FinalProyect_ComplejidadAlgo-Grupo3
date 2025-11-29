"""
Clustering Service Implementation
Refactored for DDD
"""

import numpy as np
from typing import List, Tuple, Dict, Any
from sklearn.cluster import KMeans
import time

class ClusteringService:
    def __init__(self, n_clusters: int = 5, random_state: int = 42):
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.model = None
        self.labels_ = None
        self.cluster_centers_ = None

    def fit(self, coordinates: np.ndarray) -> 'ClusteringService':
        self.model = KMeans(
            n_clusters=self.n_clusters,
            random_state=self.random_state,
            n_init=10,
            max_iter=300
        )
        self.model.fit(coordinates)
        self.labels_ = self.model.labels_
        self.cluster_centers_ = self.model.cluster_centers_
        return self

    def get_clusters(self, coordinates: np.ndarray, names: List[str]) -> List[Dict[str, Any]]:
        if self.labels_ is None:
            self.fit(coordinates)

        clusters = []
        for i in range(self.n_clusters):
            indices = np.where(self.labels_ == i)[0]
            if len(indices) == 0:
                continue
            
            coords_cluster = coordinates[indices]
            names_cluster = [names[idx] for idx in indices]
            
            clusters.append({
                'id': i,
                'coords': coords_cluster.tolist(),
                'names': names_cluster,
                'original_indices': indices.tolist(),
                'centroid': self.cluster_centers_[i].tolist() if self.cluster_centers_ is not None else None
            })
        
        return clusters

    def get_stats(self) -> Dict[str, Any]:
        if self.labels_ is None:
            return {}
        
        sizes = [int(np.sum(self.labels_ == i)) for i in range(self.n_clusters)]
        return {
            'n_clusters': self.n_clusters,
            'sizes': sizes,
            'inertia': float(self.model.inertia_) if self.model else 0
        }
