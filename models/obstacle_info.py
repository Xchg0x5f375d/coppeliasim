from typing import Optional, NamedTuple


class ObstacleInfo(NamedTuple):
    current_position: tuple[float, float]
    closest_obstacle: Optional[tuple[float, float]]
    distance: float
