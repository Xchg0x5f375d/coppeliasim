from dataclasses import dataclass
from typing import NamedTuple, Optional


@dataclass
class ObstacleInfo(NamedTuple):
    current_position: tuple[float, float]
    closest_obstacle: Optional[tuple[float, float]]
    distance: float
