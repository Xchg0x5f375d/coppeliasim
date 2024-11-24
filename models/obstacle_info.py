from typing import NamedTuple, Optional


class ObstacleInfo(NamedTuple):
    current_position: tuple[float, float]
    closest_obstacle_position: Optional[tuple[float, float]]
    distance: float
