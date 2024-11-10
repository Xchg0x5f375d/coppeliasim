import math
from dataclasses import dataclass
from typing import ClassVar, Final, List


@dataclass
class RobotConstants:
    # Wheel Dimensions (in meters)
    WHEEL_DIAMETER: Final[float] = 0.1
    WHEEL_PERIMETER: Final[float] = math.pi * WHEEL_DIAMETER

    # Robot Chassis Dimensions (in meters)
    WHEEL_DISTANCE_VERTICAL: Final[float] = (
        0.471  # Distance between front and rear wheels
    )
    WHEEL_DISTANCE_HORIZONTAL: Final[float] = (
        0.30046  # Distance between left and right wheels
    )

    MOVEMENT_CORRECTION_FACTOR: Final[float] = 1.045

    JOINT_NAMES: ClassVar[List[str]] = [
        "fl",
        "rl",
        "rr",
        "fr",
    ]

    @staticmethod
    def get_wheel_radius() -> float:
        return RobotConstants.WHEEL_DIAMETER / 2

    @staticmethod
    def get_chassis_dimensions() -> tuple[float, float]:
        return (
            RobotConstants.WHEEL_DISTANCE_VERTICAL,
            RobotConstants.WHEEL_DISTANCE_HORIZONTAL,
        )

    @staticmethod
    def get_half_wheel_distance_vertical() -> float:
        return RobotConstants.WHEEL_DISTANCE_VERTICAL / 2.0

    @staticmethod
    def get_half_wheel_distance_horizontal() -> float:
        return RobotConstants.WHEEL_DISTANCE_HORIZONTAL / 2.0

    @staticmethod
    def get_total_wheel_distance() -> float:
        return (
            RobotConstants.WHEEL_DISTANCE_VERTICAL
            + RobotConstants.WHEEL_DISTANCE_HORIZONTAL
        )
