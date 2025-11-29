from pydantic import BaseModel
from typing import List, Optional

class ManualPoint(BaseModel):
    lat: float
    lng: float
    name: str = "Manual Point"

class OptimizeRequest(BaseModel):
    n_clusters: int = 5
    method: str = 'auto'
    use_csv: bool = False
    date_filter: Optional[str] = None
    manual_points: Optional[List[ManualPoint]] = None
    max_points: int = 50
