import time
from enum import Enum
from typing import List, Optional, Tuple

import numpy as np

from constants.path_constants import PathConstants
from controllers.wheel_movement_controller import WheelMovementController
from robot.robot_position import RobotPosition
from utils.linalg_utils import LinAlgUtils
from utils.vrep_connection import VREPConnection


class PathPlanner(Enum):
    BiTRRT = 1
    BITstar = 2
    BKPIECE1 = 3
    CForest = 4
    EST = 5
    FMT = 6
    KPIECE1 = 7
    LazyPRM = 8
    LazyPRMstar = 9
    LazyRRT = 10
    LBKPIECE1 = 11
    LBTRRT = 12
    PDST = 13
    PRM = 14
    PRMstar = 15
    pRRT = 16
    pSBL = 17
    RRT = 18
    RRTConnect = 19
    RRTstar = 20
    SBL = 21
    SPARS = 22
    SPARStwo = 23
    STRIDE = 24
    TRRT = 25

    def __str__(self):
        return f"{self.value} sim_ompl_algorithm_{self.name}"


class PathPlanningController:
    def __init__(
        self,
        vrep_connection: VREPConnection,
        position: RobotPosition,
        wheel_movement_controller: WheelMovementController,
    ):
        self.vrep_connection = vrep_connection
        self.position = position
        self.wheel_movement_controller = wheel_movement_controller
        self.wheel_joints = self.wheel_movement_controller.wheel_joints

    @staticmethod
    def get_available_path_planners() -> List[str]:
        return [str(planner) for planner in PathPlanner]

    def __show_path_planners(self):
        print("\nAvailable planners")
        for planner in self.get_available_path_planners():
            print(planner)

    def __choose_path_planner(self) -> int:
        self.vrep_connection.auxiliary_console_print(
            "Path Planner Selection", "Please open the CLI to input the path planner ID"
        )
        self.__show_path_planners()
        while True:
            try:
                choice = int(
                    input("\nPlease choose a path planner by entering its number: ")
                )
                if 1 <= choice <= len(PathPlanner):
                    return choice
                else:
                    print(
                        "Invalid choice. Please enter a number between 1 and",
                        len(PathPlanner),
                    )
            except ValueError:
                print("Invalid input. Please enter a number")

    def __obtain_path_with_planner_id(
        self, script_name: str, function_name: str, planner_id: int
    ) -> Tuple[int, List[float]]:
        result = self.vrep_connection.call_script_function(
            script_name,
            function_name,
            input_ints=[planner_id],
        )
        if not result.success:
            print(f"Failed to obtain path. Error code: {result.return_code}")
            return result.return_code, []
        return result.return_code, result.output_floats

    def __turn_until_physical(self, angle: float, degree: float) -> None:
        angular_velocity = ((300.46 + 471) / 2) * angle / 50
        dt = abs(degree / angular_velocity) * 1.04
        velocities = self.wheel_movement_controller.compute_standard_wheel_velocities(
            0, 0, angle
        )
        self.wheel_movement_controller.set_wheel_velocities(velocities)
        time.sleep(dt)
        if angle <= 0:
            orientation_x = self.position.orientation_vector[0] * np.cos(
                degree * np.pi / 180.0
            ) - self.position.orientation_vector[1] * np.sin(degree * np.pi / 180.0)
            orientation_y = self.position.orientation_vector[1] * np.cos(
                degree * np.pi / 180.0
            ) + self.position.orientation_vector[0] * np.sin(degree * np.pi / 180.0)
        else:
            orientation_x = self.position.orientation_vector[0] * np.cos(
                -degree * np.pi / 180.0
            ) - self.position.orientation_vector[1] * np.sin(-degree * np.pi / 180.0)
            orientation_y = self.position.orientation_vector[1] * np.cos(
                -degree * np.pi / 180.0
            ) + self.position.orientation_vector[0] * np.sin(-degree * np.pi / 180.0)
        self.position.orientation_vector[0] = orientation_x
        self.position.orientation_vector[1] = orientation_y
        self.position.set_orientation_vector(
            LinAlgUtils.normalize_vector(self.position.get_orientation_vector())
        )

    def __get_angle_to_goal(self, goal: List[float]) -> Tuple[float, float]:
        distance_to_goal = np.sqrt(goal[0] ** 2 + goal[1] ** 2)
        norm_goal = [goal[0], goal[1]]
        norm_goal[0] /= distance_to_goal
        norm_goal[1] /= distance_to_goal
        orientation_vector = self.position.get_orientation_vector()
        angle = (
            orientation_vector[0] * norm_goal[0] + orientation_vector[1] * norm_goal[1]
        )
        angle = (angle + np.pi) % (2 * np.pi) - np.pi
        if abs(angle) > 1.0:
            print(f"Invalid angle: {angle}")
            return 0, 0
        rad = np.acos(angle)
        direction = orientation_vector[1] * goal[0] - orientation_vector[0] * goal[1]
        return rad * (180 / np.pi), direction

    def __turn_towards_goal(self, goal: List[float]) -> None:
        degree, direction = self.__get_angle_to_goal(goal)
        self.__turn_until_physical(-2 if direction < 0 else 2, degree)
        self.wheel_movement_controller.stop()

    def __follow_path(self, path: List[float]) -> None:
        path_points = LinAlgUtils.to_matrix(path, 3)
        self.position.set_relative_pos(path[:2])
        self.__turn_towards_goal(
            [
                path[3] - self.position.relative_pos[0],
                path[4] - self.position.relative_pos[1],
            ]
        )
        path = list(path_points[1::20])
        path.append(path_points[len(path_points) - 1])
        for key_point in path[1:]:
            print(f"Current Orientation: {self.position.get_orientation_vector()}")
            print(f"Relative Position: {self.position.get_relative_pos()}")
            print(f"Target Point: {key_point}")
            vector_to_point = [
                key_point[0] - self.position.relative_pos[0],
                key_point[1] - self.position.relative_pos[1],
            ]
            base_pos, base_ori = self.position.check_pose()
            self.position.set_relative_pos(base_pos[1][:2])
            self.position.set_orientation_vector(LinAlgUtils.de_eulerize(base_ori[1]))
            degree, direction = self.__get_angle_to_goal(vector_to_point)
            vector_length = LinAlgUtils.vector_length(
                [
                    key_point[0] - self.position.relative_pos[0],
                    key_point[1] - self.position.relative_pos[1],
                ]
            )
            if vector_length < PathConstants.MIN_DISTANCE_TO_POINT:
                continue
            if degree > PathConstants.LARGE_ANGLE_THRESHOLD:
                self.wheel_movement_controller.stop()
                self.__turn_towards_goal(
                    [
                        key_point[0] - self.position.relative_pos[0],
                        key_point[1] - self.position.relative_pos[1],
                    ]
                )
            while vector_length > PathConstants.MIN_DISTANCE_TO_MOVE:
                base_pos, base_ori = self.position.check_pose()
                self.position.set_relative_pos(base_pos[1][:2])
                self.position.set_orientation_vector(
                    LinAlgUtils.de_eulerize(base_ori[1])
                )
                vector_to_point = [
                    key_point[0] - self.position.relative_pos[0],
                    key_point[1] - self.position.relative_pos[1],
                ]
                vector_length = LinAlgUtils.vector_length(
                    [
                        key_point[0] - self.position.relative_pos[0],
                        key_point[1] - self.position.relative_pos[1],
                    ]
                )
                degree, direction = self.__get_angle_to_goal(vector_to_point)
                self.wheel_movement_controller.move_and_adjust(
                    degree, direction, vector_length
                )
                if degree > PathConstants.ANGLE_ADJUSTMENT_THRESHOLD:
                    break
        self.wheel_movement_controller.stop()

    def plan_and_execute_path(
        self, script_name: str, function_name: str, planner_id: Optional[int] = None
    ) -> None:
        if planner_id is None:
            planner_id = self.__choose_path_planner()
        _, path = self.__obtain_path_with_planner_id(
            script_name, function_name, planner_id
        )
        if path:
            self.__follow_path(path)
