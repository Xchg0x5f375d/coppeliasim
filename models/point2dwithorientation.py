from dataclasses import dataclass


@dataclass
class Point2DWithOrientation:
    x: float
    y: float
    yaw: float
