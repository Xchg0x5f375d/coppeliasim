import math
import time
from typing import Callable, Optional, Union

import numpy as np

from constants.robot_constants import RobotConstants
from models.movement_dynamics import MovementDynamics
from models.path_types import PathType
from models.wheel_velocities import WheelVelocities
from robot.robot_position import RobotPosition
from utils.base_connection import BaseConnection


class WheelMovementController:
    def __init__(
        self,
        vrep_connection: BaseConnection,
        position: RobotPosition,
        wheel_joints: np.ndarray,
    ):
        self.vrep_connection = vrep_connection
        self.position = position
        self.wheel_joints = wheel_joints

    @staticmethod
    def __calculate_movement_time(distance: float, speed: float) -> float:
        return (
            (distance / RobotConstants.WHEEL_PERIMETER)
            * (2 * math.pi / abs(speed))
            * RobotConstants.MOVEMENT_CORRECTION_FACTOR
        )

    @staticmethod
    def __calculate_turn_time(degree: float, speed: float) -> float:
        return (
            (
                (RobotConstants.get_total_wheel_distance())
                / RobotConstants.WHEEL_PERIMETER
            )
            * math.pi
            * (abs(degree) / abs(speed))
            * (math.pi / 180)
        )

    def __handle_velocity_change(
        self,
        speed: float,
        duration: float,
        accelerating: bool,
        velocity_calculator: Optional[
            Callable[[float, float, float], WheelVelocities]
        ] = None,
    ) -> None:
        dt = 0.05
        steps = int(duration / dt)
        if velocity_calculator is None:
            velocity_calculator = self.compute_standard_wheel_velocities
        for step in range(steps):
            progress = (step / steps) if accelerating else (1 - (step / steps))
            current_speed = speed * progress
            velocities = velocity_calculator(current_speed, 0, 0)
            self.set_wheel_velocities(velocities)
            time.sleep(dt)

    @staticmethod
    def __compute_path_velocity_scale(
        angle: Optional[float], path_type: PathType
    ) -> float:
        if angle is not None and path_type == "ellipse":
            return 1.0 + 0.2 * math.cos(2 * angle)
        return 1.0

    def set_wheel_velocities(
        self, velocities: Union[float, np.ndarray, WheelVelocities]
    ) -> None:
        if isinstance(velocities, (int, float)):
            velocities = [velocities] * 4
        elif isinstance(velocities, WheelVelocities):
            velocities = velocities.to_array()
        for i, velocity in enumerate(velocities):
            self.vrep_connection.set_joint_target_velocity(
                self.wheel_joints[i], velocity
            )

    def move_forward(
        self,
        distance: float,
        speed: float,
        dynamics: Union[str, MovementDynamics] = MovementDynamics.CONSTANT,
    ) -> None:
        if isinstance(dynamics, str):
            dynamics = MovementDynamics(dynamics)
        if speed < 0:
            raise ValueError(
                "Speed should be positive, use negative distance for backward movement"
            )
        actual_speed = -speed if distance < 0 else speed
        self.set_wheel_velocities(0)
        movement_time = self.__calculate_movement_time(abs(distance), speed)
        if dynamics == MovementDynamics.CONSTANT:
            velocities = self.compute_standard_wheel_velocities(actual_speed, 0, 0)
            self.set_wheel_velocities(velocities)
            time.sleep(movement_time)
        elif dynamics == MovementDynamics.ACCELERATE:
            self.accelerate(actual_speed, movement_time)
        elif dynamics == MovementDynamics.DECELERATE:
            self.decelerate(actual_speed, movement_time)
        elif dynamics == MovementDynamics.ACCEL_DECEL:
            self.accelerate(actual_speed, movement_time)
            self.decelerate(actual_speed, movement_time)
        self.set_wheel_velocities(0)
        self.position.odometry(0, distance)

    def turn_right(
        self,
        degree: float,
        speed: float,
        dynamics: Union[str, MovementDynamics] = MovementDynamics.CONSTANT,
    ) -> None:
        self.set_wheel_velocities(0)
        turn_time = self.__calculate_turn_time(degree, speed)
        rotation_speed = -speed if degree < 0 else speed
        if dynamics == MovementDynamics.CONSTANT:
            velocities = self.compute_standard_wheel_velocities(0, 0, rotation_speed)
            self.set_wheel_velocities(velocities)
            time.sleep(turn_time)
        elif dynamics == MovementDynamics.ACCELERATE:
            self.accelerate(rotation_speed, turn_time)
        elif dynamics == MovementDynamics.DECELERATE:
            self.decelerate(rotation_speed, turn_time)
        elif dynamics == MovementDynamics.ACCEL_DECEL:
            self.accelerate(rotation_speed, turn_time)
            self.decelerate(rotation_speed, turn_time)
        self.set_wheel_velocities(0)
        self.position.odometry(degree, 0)

    def accelerate(
        self,
        speed: float,
        duration: float,
        velocity_calculator: Optional[
            Callable[[float, float, float], WheelVelocities]
        ] = None,
    ) -> None:
        accel_duration = 0.5 * duration
        self.__handle_velocity_change(speed, accel_duration, True, velocity_calculator)

    def decelerate(
        self,
        speed: float,
        movement_time: float,
        velocity_calculator: Optional[
            Callable[[float, float, float], WheelVelocities]
        ] = None,
    ) -> None:
        decel_duration = 0.5 * movement_time
        self.__handle_velocity_change(speed, decel_duration, False, velocity_calculator)

    @staticmethod
    def compute_standard_wheel_velocities(
        forw_back_vel: float, left_right_vel: float, rot_vel: float
    ) -> np.ndarray:
        front_left = forw_back_vel - left_right_vel - rot_vel
        rear_left = forw_back_vel - left_right_vel - rot_vel
        rear_right = forw_back_vel + left_right_vel + rot_vel
        front_right = forw_back_vel + left_right_vel + rot_vel
        return np.array([front_left, rear_left, rear_right, front_right])

    @staticmethod
    def compute_mecanum_wheel_velocities(
        forw_back_vel: float,
        left_right_vel: float,
        rot_vel: float,
        velocity_scale: float = 1.0,
    ) -> np.ndarray:
        l = RobotConstants.get_half_wheel_distance_vertical()
        w = RobotConstants.get_half_wheel_distance_horizontal()
        r = RobotConstants.get_wheel_radius()
        wheel_factor = 1 / r
        moment_arm = l + w
        front_left = (
            wheel_factor
            * (forw_back_vel - left_right_vel - moment_arm * rot_vel)
            * velocity_scale
        )
        rear_left = (
            wheel_factor
            * (forw_back_vel + left_right_vel - moment_arm * rot_vel)
            * velocity_scale
        )
        rear_right = (
            wheel_factor
            * (forw_back_vel + left_right_vel + moment_arm * rot_vel)
            * velocity_scale
        )
        front_right = (
            wheel_factor
            * (forw_back_vel - left_right_vel + moment_arm * rot_vel)
            * velocity_scale
        )
        return np.array([front_left, rear_left, rear_right, front_right])

    def calculate_path_adjusted_mecanum_velocities(
        self,
        forw_back_vel: float,
        left_right_vel: float,
        rot_vel: float,
        angle: Optional[float] = None,
        path_type: PathType = "circle",
    ) -> np.ndarray:
        velocity_scale = self.__compute_path_velocity_scale(angle, path_type)
        return self.compute_mecanum_wheel_velocities(
            forw_back_vel, left_right_vel, rot_vel, velocity_scale
        )
