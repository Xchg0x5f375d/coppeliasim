from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class ObstacleDetectionResult:
    obstacles: List[Tuple[float, float]]
    should_stop: bool
    latest_obstacle: Optional[Tuple[float, float]] = None
    latest_obstacle_distance: Optional[float] = None

    def has_latest_obstacle(self) -> bool:
        return (
            self.latest_obstacle is not None
            and self.latest_obstacle_distance is not None
        )
