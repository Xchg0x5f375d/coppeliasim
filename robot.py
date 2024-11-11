from typing import List, Optional

import numpy as np

from arm_movement_controller import ArmMovementController
from robot_constants import RobotConstants
from robot_position import RobotPosition
from vrep_connection import VREPConnection
from wheel_movement_controller import WheelMovementController


class Robot:
    def __init__(
        self,
        vrep_connection: VREPConnection = VREPConnection(),
        position: RobotPosition = RobotPosition(),
    ):
        self.vrep_connection = vrep_connection
        self.wheel_joints = self.__initialize_wheel_joints()
        self.arm_joints = self.__initialize_arm_joints()
        self.position = position
        self.__validate_initialization()
        self.__setup_controllers()

    def set_position(self, position: RobotPosition = RobotPosition()) -> None:
        self.vrep_connection.set_object_position("youBot", position.to_position_tuple())

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
            handle = self.vrep_connection.get_object_handle(f"youBotArmJoint{i}")
            if handle is None:
                return False
            self.arm_joints[i] = handle
        return self.arm_joints

    def __validate_initialization(self) -> None:
        if self.wheel_joints is None:
            raise Exception("Failed to initialize wheel joints")

        if self.arm_joints is None:
            raise Exception("Failed to initialize arm joints")

    def __setup_controllers(self) -> None:
        self.wheel_movement_controller = WheelMovementController(
            self.vrep_connection, self.wheel_joints
        )
        self.arm_movement_controller = ArmMovementController(
            self.vrep_connection, self.arm_joints
        )

    def __del__(self):
        del self.vrep_connection
