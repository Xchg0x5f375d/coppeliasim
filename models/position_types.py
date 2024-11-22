from typing import TypeAlias, Optional

Position: TypeAlias = tuple[float, float]
Obstacle: TypeAlias = tuple[float, float]
ObstacleResult: TypeAlias = tuple[Position, Optional[Obstacle]]
