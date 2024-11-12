from enum import Enum


class MovementDynamics(Enum):
    CONSTANT = "constant"
    ACCELERATE = "accel"
    DECELERATE = "decel"
    ACCEL_DECEL = "accel_decel"
