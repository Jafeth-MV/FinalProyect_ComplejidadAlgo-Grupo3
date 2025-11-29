import numpy as np
from domain.services.tsp_service import TSPService

def test_manual_mode():
    service = TSPService()
    
    # Simulate 3 points in Peru (Lima, Ica, Huancayo approx)
    coords = np.array([
        [-12.0464, -77.0428], # Lima
        [-14.0678, -75.7286], # Ica
        [-12.0651, -75.2049]  # Huancayo
    ])
    
    print("Testing Brute Force with 3 points...")
    route, dist, stats = service.solve(coords, method='brute_force')
    
    print(f"Route: {route}")
    print(f"Distance: {dist}")
    print(f"Stats: {stats}")

if __name__ == "__main__":
    test_manual_mode()
