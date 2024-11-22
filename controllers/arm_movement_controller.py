import time
from typing import List, Tuple

from utils.base_connection import BaseConnection


class ArmMovementController:
    def __init__(self, vrep_connection: BaseConnection, arm_joints: List[int]):
        self.vrep_connection = vrep_connection
        self.arm_joints = arm_joints

    def move_arm(self, joint_movements: List[Tuple[int, float]]):
        for joint_idx, angle in joint_movements:
            self.vrep_connection.set_joint_target_position(
                self.arm_joints[joint_idx], angle
            )
            time.sleep(1)
