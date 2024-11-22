import math
import time
from typing import List, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np

from constants import RobotConstants
from robot.robot_position import RobotPosition
from utils import vrep
from utils.base_connection import BaseConnection


class SensorController:
    def __init__(
        self, vrep_connection: BaseConnection, position: RobotPosition
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
        self.__read_sensors_streaming()
        self.__read_sensors_buffer()
        self.__read_sensors_blocking()

    @staticmethod
    def __get_distance(aux_data: List, n: int) -> float:
        return aux_data[1][4 * n + 5]

    def __read_sensors_streaming(self) -> Tuple[List[List[float]], List[List[float]]]:
        _, _, aux_data1 = self.vrep_connection.read_vision_sensor(
            self.hokuyo1_handle, operation_mode=vrep.simx_opmode_streaming
        )
        _, _, aux_data2 = self.vrep_connection.read_vision_sensor(
            self.hokuyo2_handle, operation_mode=vrep.simx_opmode_streaming
        )
        return aux_data1, aux_data2

    def __read_sensors_buffer(self) -> Tuple[List[List[float]], List[List[float]]]:
        _, _, aux_data1 = self.vrep_connection.read_vision_sensor(
            self.hokuyo1_handle, operation_mode=vrep.simx_opmode_buffer
        )
        _, _, aux_data2 = self.vrep_connection.read_vision_sensor(
            self.hokuyo2_handle, operation_mode=vrep.simx_opmode_buffer
        )
        return aux_data1, aux_data2

    def __read_sensors_blocking(self) -> None:
        self.vrep_connection.read_vision_sensor(self.hokuyo1_handle)
        self.vrep_connection.read_vision_sensor(self.hokuyo2_handle)

    def get_distances(self) -> Tuple[float, float, float]:
        _, _, aux_data1 = self.vrep_connection.read_vision_sensor(self.hokuyo1_handle)
        _, _, aux_data2 = self.vrep_connection.read_vision_sensor(self.hokuyo2_handle)
        last_index = int(len(aux_data1[1]) / 4) - 1
        left_distance = self.__get_distance(aux_data2, int(last_index * (90 / 120)))
        front_distance = self.__get_distance(aux_data1, last_index)
        right_distance = self.__get_distance(aux_data1, int(last_index * (30 / 120)))
        return left_distance, front_distance, right_distance

    def detect_obstacles(self, threshold=5.0) -> List[Tuple[float, float]]:
        aux_data1, _ = self.__read_sensors_streaming()
        time.sleep(0.01)
        aux_data1, _ = self.__read_sensors_buffer()
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

    def plot_obstacles(
        self, title: str = "", save_path: Optional[str] = "image.png"
    ) -> None:
        x = [obs[0] for obs in self.obstacles]
        y = [obs[1] for obs in self.obstacles]
        plt.figure(figsize=(10, 10))
        plt.plot(x, y, "ko", label="Obstacles", markersize=5)
        plt.plot(
            self.position.local_x,
            self.position.local_y,
            "r*",
            label=RobotConstants.YOUBOT_NAME,
            markersize=10,
        )
        arrow_length = 0.3
        plt.quiver(
            self.position.local_x,
            self.position.local_y,
            arrow_length * np.cos(self.position.local_yaw),
            arrow_length * np.sin(self.position.local_yaw),
            color="red",
            scale=1,
            scale_units="xy",
            angles="xy",
            width=0.02,
            alpha=0.8,
            zorder=5,
        )
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.minorticks_on()
        plt.grid(True, which="minor", linestyle=":", alpha=0.4)
        plt.axis("equal")
        plt.gca().invert_yaxis()
        plt.title(title, pad=20, fontsize=12)
        plt.xlabel("X Position (m)", labelpad=10)
        plt.ylabel("Y Position (m)", labelpad=10)
        plt.legend(loc="upper right", framealpha=0.9)
        plt.tight_layout()
        if save_path:
            plt.savefig(f"docs/{save_path}")
        plt.show()
