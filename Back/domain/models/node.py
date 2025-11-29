from dataclasses import dataclass

@dataclass
class Node:
    id: str
    lat: float
    lon: float
    name: str
