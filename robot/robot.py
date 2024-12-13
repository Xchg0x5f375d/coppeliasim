from typing import List, Optional

import numpy as np

from constants.robot_constants import RobotConstants
from controllers.arm_movement_controller import ArmMovementController
from robot.robot_position import RobotPosition
from utils import VREPConnection
from utils.base_connection import BaseConnection


class Robot:
    def __init__(
        self,
        vrep_connection: Optional[BaseConnection] = None,
        position: Optional[RobotPosition] = None,
    ):
        self.vrep_connection = (
            VREPConnection() if vrep_connection is None else vrep_connection
        )
        self.position = self.__initialize_position(position)
        self.wheel_joints = self.__initialize_wheel_joints()
        self.arm_joints = self.__initialize_arm_joints()
        self.__validate_initialization()
        self.__setup_controllers()

    def __initialize_wheel_joints(self) -> Optional[np.ndarray]:
        self.wheel_joints = np.empty(4, dtype=int)
        self.wheel_joints.fill(-1)
        for i, joint in enumerate(RobotConstants.JOINT_NAMES):
            status, handle = self.vrep_connection.get_object_handle(
                f"rollingJoint_{joint}"
            )
            if handle is None:
                print(
                    f"Failed to get handle for rollingJoint_{joint}: error code {status}"
                )
                return None
            self.wheel_joints[i] = handle
        return self.wheel_joints

    def __initialize_arm_joints(self) -> Optional[List[int]]:
        self.arm_joints = [0] * 5
        for i in range(5):
            _, handle = self.vrep_connection.get_object_handle(
                f"{RobotConstants.YOUBOT_NAME}ArmJoint{i}"
            )
            if handle is None:
                return None
            self.arm_joints[i] = handle
        return self.arm_joints

    def __validate_initialization(self) -> None:
        if self.wheel_joints is None:
            raise Exception("Failed to initialize wheel joints")
        if self.arm_joints is None:
            raise Exception("Failed to initialize arm joints")

    def __initialize_position(
        self, position: Optional[RobotPosition] = None
    ) -> RobotPosition:
        if position is None:
            return RobotPosition(self.vrep_connection)
        return position

    def __setup_controllers(self) -> None:
        from controllers.sensor_controller import SensorController
        from controllers.wheel_movement_controller import WheelMovementController

        self.sensor_controller = SensorController(self.vrep_connection, self.position)
        self.wheel_movement_controller = WheelMovementController(
            self.vrep_connection,
            self.position,
            self.wheel_joints,
            self.sensor_controller,
        )
        self.arm_movement_controller = ArmMovementController(
            self.vrep_connection, self.arm_joints
        )

    def __del__(self):
        del self.vrep_connection
