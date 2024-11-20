import math
from typing import List, Optional, Tuple

import matplotlib.pyplot as plt

from robot.robot_position import RobotPosition
from utils.vrep_connection import VREPConnection


class SensorController:
    def __init__(
        self, vrep_connection: VREPConnection, position: RobotPosition
    ) -> None:
        self.vrep_connection = vrep_connection
        self.position = position
        self.hokouyo1_handle: Optional[Tuple[int, int]] = None
        self.hokouyo2_handle: Optional[Tuple[int, int]] = None
        self.__initialize_sensors()

    def __initialize_sensors(self) -> None:
        self.vrep_connection.set_integer_signal(("handle_xy_sensor", 2))
        self.vrep_connection.set_integer_signal(("displaylasers", 1))
        status1, self.hokouyo1_handle = self.vrep_connection.get_object_handle(
            "fastHokuyo_sensor1"
        )
        status2, self.hokouyo2_handle = self.vrep_connection.get_object_handle(
            "fastHokuyo_sensor2"
        )
        if status1 != 0 or status2 != 0:
            raise Exception("Failed to initialize Hokuyo sensors")
        print("Hokuyo sensors initialized")

    @staticmethod
    def __get_distance(aux_data: List[List[float]], n: int) -> float:
        return aux_data[1][4 * n + 5]

    def get_left_front_right_distances(self) -> Tuple[float, float, float]:
        _, _, aux_data1 = self.vrep_connection.read_vision_sensor(self.hokouyo1_handle)
        _, _, aux_data2 = self.vrep_connection.read_vision_sensor(self.hokouyo2_handle)

        if not aux_data1 or not aux_data2:
            return -1.0, -1.0, -1.0

        last_index = int(len(aux_data1[1]) / 4) - 1

        left_distance = self.__get_distance(aux_data1, int(last_index * (30 / 120)))
        front_distance = self.__get_distance(aux_data1, last_index)
        right_distance = self.__get_distance(aux_data2, int(last_index * (90 / 120)))

        return left_distance, front_distance, right_distance

    def detect_obstacles(self, threshold=5.0) -> List[Tuple[float, float]]:
        _, _, aux_data1 = self.vrep_connection.read_vision_sensor(self.hokouyo1_handle)
        obstacles: List[Tuple[float, float]] = []

        last_index = int(len(aux_data1) / 4 - 1)
        front_distance = self.__get_distance(aux_data1, last_index)

        if front_distance < threshold:
            x = self.position.local_x + front_distance * math.cos(
                self.position.local_yaw
            )
            y = self.position.local_y + front_distance * math.sin(
                self.position.local_yaw
            )
            obstacles.append((x, y))

        return obstacles

    def print_distances(self) -> None:
        left, front, right = self.get_left_front_right_distances()
        print("\nRead sensors\n")
        print("Distance Left: " + str(left))
        print("Distance Front: " + str(front))
        print("Distance Right: " + str(right) + "\n")

    def visualize_obstacles(
        self, obstacles: List[Tuple[float, float]], save_path: Optional[str] = None
    ) -> None:
        x_coords = [obs[0] for obs in obstacles]
        y_coords = [obs[1] for obs in obstacles]

        plt.figure(figsize=(10, 10))
        plt.plot(x_coords, y_coords, "ko", label="Obstacles")
        plt.plot(self.position.x, self.position.y, "r*", label="Robot Position")

        plt.grid(True)
        plt.axis("equal")
        plt.title("Obstacle Detection Results")
        plt.xlabel("X Position (m)")
        plt.ylabel("Y Position (m)")
        plt.legend()

        if save_path:
            plt.savefig(save_path)
        plt.show()
