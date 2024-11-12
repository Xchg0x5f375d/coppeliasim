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
        self.vrep_connection.get_ping_time()
        return base_pos, base_orient

    def print_position(self) -> None:
        pos, orient = self.check_pose()
        global_x, local_x = np.round(pos[1][0], 5), np.round(self.local_x, 5)
        global_y, local_y = np.round(pos[1][1], 5), np.round(self.local_y, 5)
        global_yaw, local_yaw = np.round(orient[1][2], 5), np.round(self.local_yaw)
        messages = (
            f"Global [PosX, PosY, AngZ]: {global_x}, {global_y}, {global_yaw}\n",
            f"Local [PosX, PosY, AngZ]: {local_x}, {local_y}, {local_yaw}",
        )
        for message in messages:
            print(message)

    def odometry(self, angle_r: float, distance_r: float) -> None:
        self.local_yaw += angle_r
        self.local_x += distance_r * math.cos(self.local_yaw)
        self.local_y += distance_r * math.sin(self.local_yaw)
