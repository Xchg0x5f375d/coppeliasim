import math
from typing import Tuple

import numpy as np

from constants.robot_constants import RobotConstants
from utils.vrep_connection import VREPConnection


class RobotPosition:
    def __init__(
        self,
        vrep_connection: VREPConnection,
        x: float = 0.0,
        y: float = 0.0,
        yaw: float = 0.0,
    ):
        self.vrep_connection = vrep_connection
        self.x = x
        self.y = y
        self.yaw = yaw

        self.local_x = 0.0
        self.local_y = 0.0
        self.local_yaw = 0.0

    def set_position(
        self,
        position: Tuple[float, float, float] | float | int = (-4.700, 0.200, 0.0957),
    ) -> None:
        if isinstance(position, (float, int)):
            position = (float(position),) * 3
        elif len(position) != 3:
            raise ValueError("Position must be a tuple of 3 coordinates")
        self.vrep_connection.set_object_position(
            RobotConstants.YOUBOT_NAME, self.to_position_tuple()
        )

    def to_position_tuple(self) -> tuple[float, float, float]:
        return (self.x, self.y, self.yaw)

    def check_pose(self) -> tuple[tuple[int, list], tuple[int, list]]:
        _, handle = self.vrep_connection.get_object_handle(RobotConstants.YOUBOT_NAME)
        base_pos = self.vrep_connection.get_object_position(handle)
        base_orient = self.vrep_connection.get_object_orientation(handle)
        if base_pos[0] != -1:
            self.x = np.round(base_pos[1][0], 5)
            self.y = np.round(base_pos[1][1], 5)
        if base_orient[0] != -1:
            self.yaw = np.round(base_orient[1][2], 5)
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
        angle_rad = math.radians(angle_deg)
        self.local_yaw += math.atan2(math.sin(angle_rad), math.cos(angle_rad))
        self.local_x += distance * math.cos(self.local_yaw)
        self.local_y += distance * math.sin(self.local_yaw)

    def print_position(self) -> None:
        global_pos, local_pos = self.get_position()
        print(global_pos, local_pos, sep="\n")
