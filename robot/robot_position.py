import math
from typing import Tuple

import numpy as np
from numpy import ndarray

from constants.robot_constants import RobotConstants
from utils.vrep_connection import VREPConnection


class RobotPosition:
    def __init__(
        self,
        vrep_connection: VREPConnection,
        x: float = -4.700,
        y: float = 0.200,
        yaw: float = -1.57093,
    ):
        self.vrep_connection = vrep_connection
        self.local_x = x
        self.local_y = y
        self.local_yaw = yaw

    def set_position(
        self,
        position: Tuple[float, float, float] | float | int = (-4.700, 0.200, 0.0957),
    ) -> None:
        if isinstance(position, (float, int)):
            position = (float(position),) * 3
        elif len(position) != 3:
            raise ValueError("Position must be a tuple of 3 coordinates")
        self.local_x, self.local_y, self.local_yaw = position
        self.vrep_connection.set_object_position(RobotConstants.YOUBOT_NAME, position)

    def to_position_tuple(self) -> tuple[float, float, float]:
        return self.local_x, self.local_y, self.local_yaw

    def check_pose(self) -> tuple[tuple[int, ndarray], tuple[int, ndarray]]:
        _, handle = self.vrep_connection.get_object_handle(RobotConstants.YOUBOT_NAME)
        base_pos = self.vrep_connection.get_object_position(handle)
        base_orient = self.vrep_connection.get_object_orientation(handle)
        self.vrep_connection.get_ping_time()
        return base_pos, base_orient

    def get_position(self) -> tuple[str, str]:
        pos, orient = self.check_pose()
        global_pos = (
            f"global [PosX, PosY, AngZ]: "
            f"{np.round(pos[1][0], 5)}, "
            f"{np.round(pos[1][1], 5)}, "
            f"{np.round(orient[1][2], 5)}"
        )
        local_pos = (
            f"local [PosX, PosY, AngZ]: "
            f"{np.round(self.local_x, 5)}, "
            f"{np.round(self.local_y, 5)}, "
            f"{np.round(self.local_yaw, 5)}"
        )
        return global_pos, local_pos

    def odometry(self, angle_deg: float, distance: float) -> None:
        self.local_yaw += math.radians(angle_deg)
        self.local_yaw = math.atan2(math.sin(self.local_yaw), math.cos(self.local_yaw))
        self.local_x += distance * math.cos(self.local_yaw)
        self.local_y += distance * math.sin(self.local_yaw)

    def print_position(self) -> None:
        global_pos, local_pos = self.get_position()
        print(global_pos, local_pos, sep="\n")

    def debug_movement(self, distance: float) -> None:
        print("\nDetailed Movement Analysis:")
        print("Current Position:")
        print(
            f"(x={self.local_x:.4f}, y={self.local_y:.4f}, yaw={math.degrees(self.local_yaw):.4f}°)"
        )
        dx = distance * math.cos(self.local_yaw)
        dy = distance * math.sin(self.local_yaw)
        print("\nCalculated Movement:")
        print(f"Distance: {distance}m at angle: {math.degrees(self.local_yaw):.4f}°")
        print(f"Expected dx: {dx:.4f}m")
        print(f"Expected dy: {dy:.4f}m")
        print(
            f"Expected new position: ({self.local_x + dx:.4f}, {self.local_y + dy:.4f})"
        )
        base_pos, base_orient = self.check_pose()
        print("\nSimulator Position:")
        print(
            f"x={base_pos[1][0]:.4f}, y={base_pos[1][1]:.4f}, yaw={math.degrees(base_orient[1][2]):.4f}°"
        )
