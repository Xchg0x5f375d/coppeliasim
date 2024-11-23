import math
import time
from typing import List, Optional, Tuple

from models.obstacle_info import ObstacleInfo
from robot.robot_position import RobotPosition
from utils import vrep
from utils.base_connection import BaseConnection


class SensorController:
    def __init__(
        self,
        vrep_connection: BaseConnection,
        position: RobotPosition,
    ) -> None:
        self.vrep_connection = vrep_connection
        self.position = position
        self.obstacles: List[Tuple[float, float]] = []
        self.hokuyo1_handle: Optional[Tuple[int, int]] = None
        self.hokuyo2_handle: Optional[Tuple[int, int]] = None
        self.__initialize_sensors()

    def __initialize_sensors(self) -> None:
        self.vrep_connection.set_integer_signal(("handle_xy_sensor", 2))
        self.vrep_connection.set_integer_signal(("displaylasers", 1))
        _, self.hokuyo1_handle = self.vrep_connection.get_object_handle(
            "fastHokuyo_sensor1"
        )
        _, self.hokuyo2_handle = self.vrep_connection.get_object_handle(
            "fastHokuyo_sensor2"
        )
        self.read_sensors_streaming()
        self.read_sensors_buffer()
        self.read_sensors_blocking()

    @staticmethod
    def __get_distance(aux_data: List, n: int) -> float:
        return aux_data[1][4 * n + 5]

    def read_sensors_streaming(self) -> Tuple[List[List[float]], List[List[float]]]:
        _, _, aux_data1 = self.vrep_connection.read_vision_sensor(
            self.hokuyo1_handle, operation_mode=vrep.simx_opmode_streaming
        )
        _, _, aux_data2 = self.vrep_connection.read_vision_sensor(
            self.hokuyo2_handle, operation_mode=vrep.simx_opmode_streaming
        )
        return aux_data1, aux_data2

    def read_sensors_buffer(self) -> Tuple[List[List[float]], List[List[float]]]:
        _, _, aux_data1 = self.vrep_connection.read_vision_sensor(
            self.hokuyo1_handle, operation_mode=vrep.simx_opmode_buffer
        )
        _, _, aux_data2 = self.vrep_connection.read_vision_sensor(
            self.hokuyo2_handle, operation_mode=vrep.simx_opmode_buffer
        )
        return aux_data1, aux_data2

    def read_sensors_blocking(self) -> Tuple[List[List[float]], List[List[float]]]:
        _, _, aux_data1 = self.vrep_connection.read_vision_sensor(self.hokuyo1_handle)
        _, _, aux_data2 = self.vrep_connection.read_vision_sensor(self.hokuyo2_handle)
        return aux_data1, aux_data2

    def get_left_front_right_distances(self) -> Tuple[float, float, float]:
        _, _, aux_data1 = self.vrep_connection.read_vision_sensor(self.hokuyo1_handle)
        _, _, aux_data2 = self.vrep_connection.read_vision_sensor(self.hokuyo2_handle)
        last_index = int(len(aux_data1[1]) / 4) - 1
        left_distance = self.__get_distance(aux_data2, int(last_index * (90 / 120)))
        front_distance = self.__get_distance(aux_data1, last_index)
        right_distance = self.__get_distance(aux_data1, int(last_index * (30 / 120)))
        return left_distance, front_distance, right_distance

    def detect_obstacles(self, threshold=5.0) -> List[Tuple[float, float]]:
        self.read_sensors_streaming()
        time.sleep(0.01)
        aux_data1, _ = self.read_sensors_buffer()
        if not aux_data1 or not aux_data1[1]:
            return []
        last_index = int(len(aux_data1[1]) / 4) - 1
        front_distance = self.__get_distance(aux_data1, last_index)
        if front_distance < threshold:
            x = self.position.local_x + front_distance * math.cos(
                self.position.local_yaw
            )
            y = self.position.local_y + front_distance * math.sin(
                self.position.local_yaw
            )
            self.obstacles.append((round(x, 5), round(y, 5)))
        return self.obstacles

    def find_closest_obstacle(self) -> ObstacleInfo:
        distances = [
            math.sqrt(
                (obstacle[0] - self.position.local_x) ** 2
                + (obstacle[1] - self.position.local_y) ** 2
            )
            for obstacle in self.obstacles
        ]
        current_pos = (self.position.local_x, self.position.local_y)
        if not distances:
            return ObstacleInfo(current_pos, None, float("inf"))
        min_distance = min(distances)
        closest_idx = distances.index(min_distance)
        closest_obstacle = self.obstacles[closest_idx]
        return ObstacleInfo(current_pos, closest_obstacle, min_distance)

    def __str__(self) -> str:
        left, front, right = self.get_left_front_right_distances()
        return (
            f"\nRead sensors\n"
            f"Left Distance: {left:.3f}m\n"
            f"Front Distance: {front:.3f}m\n"
            f"Right Distance: {right:.3f}m\n"
            f"Detected Obstacles: {len(self.obstacles)}"
        )

    def __repr__(self) -> str:
        return (
            f"SensorController("
            f"position={self.position}, "
            f"obstacles={self.obstacles}, "
            f"hokuyo1_handle={self.hokuyo1_handle}, "
            f"hokuyo2_handle={self.hokuyo2_handle})"
        )
