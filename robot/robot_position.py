import math
from typing import List, Optional, Tuple

import numpy as np
from numpy import ndarray

from constants.robot_constants import RobotConstants
from models.point2d_with_orientation import Point2DWithOrientation
from utils.base_connection import BaseConnection
from utils.linalg_utils import LinAlgUtils


class RobotPosition:

    def __init__(
        self,
        vrep_connection: BaseConnection,
        x: float = -4.700,
        y: float = 0.200,
        yaw: float = -1.57093,
    ):
        self.vrep_connection = vrep_connection
        self.local_x = x
        self.local_y = y
        self.local_yaw = yaw
        self.orientation_vector = [0.0, -1.0]
        self.start_pos: List[float] = []
        self.start_ori: Optional[float] = None
        self.global_degrees = 0.0
        self.relative_pos: List[float] = [0.0, 0.0]
        self.__initialize_positions()

    def __initialize_positions(self) -> None:
        base_pos, base_orient = self.check_pose()
        self.local_x = base_pos[1][0]
        self.local_y = base_pos[1][1]
        self.local_yaw = base_orient[1][2]
        self.start_pos = base_pos[1][:2]
        self.relative_pos = base_pos[1][:2]
        self.orientation_vector = LinAlgUtils.de_eulerize(base_orient[1])
        self.start_ori = self.calculate_orientation_angle()

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

    def to_position_tuple_2d(self) -> tuple[float, float]:
        return self.local_x, self.local_y

    def to_point2d_with_orientation(self) -> Point2DWithOrientation:
        return Point2DWithOrientation(self.local_x, self.local_y, self.local_yaw)

    def check_pose(self) -> tuple[tuple[int, ndarray], tuple[int, ndarray]]:
        _, handle = self.vrep_connection.get_object_handle(RobotConstants.YOUBOT_NAME)
        base_pos = self.vrep_connection.get_object_position(handle)
        base_orient = self.vrep_connection.get_object_orientation(handle)
        self.vrep_connection.get_ping_time()
        return base_pos, base_orient

    def odometry(self, angle_deg: float, distance: float) -> None:
        self.local_yaw += math.radians(angle_deg)
        self.local_yaw = math.atan2(math.sin(self.local_yaw), math.cos(self.local_yaw))
        self.local_x += distance * math.cos(self.local_yaw)
        self.local_y += distance * math.sin(self.local_yaw)
        self.relative_pos[0] = self.local_x
        self.relative_pos[1] = self.local_y
        self.orientation_vector[0] = math.cos(self.local_yaw)
        self.orientation_vector[1] = math.sin(self.local_yaw)

    def calculate_orientation_angle(self):
        orientation_vector = self.get_orientation_vector()
        if orientation_vector[1] >= 0:
            if orientation_vector[0] >= 0:
                angle = np.arcsin(orientation_vector[0])
            else:
                angle = np.pi / 2 + abs(np.arcsin(orientation_vector[0]))
        else:
            if orientation_vector[0] >= 0:
                angle = np.pi * 2 - abs(np.arcsin(orientation_vector[0]))
            else:
                angle = np.pi + abs(np.arcsin(orientation_vector[0]))
        return angle

    def get_orientation_vector(self) -> List[float]:
        return self.orientation_vector

    def set_orientation_vector(self, orientation_vector: List[float] | ndarray) -> None:
        if isinstance(orientation_vector, ndarray):
            orientation_vector = orientation_vector.tolist()
        self.orientation_vector = orientation_vector

    def get_start_pos(self) -> List[float]:
        return self.start_pos

    def get_start_ori(self) -> Optional[float]:
        return self.start_ori

    def get_global_degrees(self) -> float:
        return self.global_degrees

    def set_global_degrees(self, global_degrees: float) -> None:
        self.global_degrees = global_degrees

    def get_relative_pos(self) -> List[float]:
        return self.relative_pos

    def set_relative_pos(self, relative_pos: List[float] | ndarray) -> None:
        if isinstance(relative_pos, ndarray):
            relative_pos = relative_pos.tolist()
        self.relative_pos = relative_pos

    def __str__(self) -> str:
        base_pos, base_orient = self.check_pose()
        return (
            f"Global [PosX, PosY, AngZ]: "
            f"{np.round(base_pos[1][0], 5)}, "
            f"{np.round(base_pos[1][1], 5)}, "
            f"{np.round(base_orient[1][2], 5)}\n"
            f"Local [PosX, PosY, AngZ]: "
            f"{np.round(self.local_x, 5)}, "
            f"{np.round(self.local_y, 5)}, "
            f"{np.round(self.local_yaw, 5)}"
        )

    def __repr__(self) -> str:
        return (
            f"RobotPosition("
            f"vrep_connection={self.vrep_connection!r}, "
            f"x={self.local_x}, "
            f"y={self.local_y}, "
            f"yaw={self.local_yaw})"
        )

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
