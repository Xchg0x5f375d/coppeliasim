from dataclasses import dataclass


@dataclass
class PathConstants:
    MIN_DISTANCE_TO_POINT = 0.4
    LARGE_ANGLE_THRESHOLD = 90
    MIN_DISTANCE_TO_MOVE = 0.3
    ANGLE_ADJUSTMENT_THRESHOLD = 45
