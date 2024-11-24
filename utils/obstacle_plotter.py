from typing import List, Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np

from constants import RobotConstants
from models import Point2DWithOrientation
from models.obstacle_info import ObstacleInfo


class ObstaclePlotter:
    def __init__(self):
        self.fig = None
        self.ax = None
        self.is_interactive = False
        self.robot_marker = None
        self.obstacle_dots = None
        self.orientation_arrow = None
        self.ray_line = None

    @staticmethod
    def __setup_plot_formatting(ax: plt.Axes, title: str) -> None:
        ax.grid(True, linestyle="--", alpha=0.7)
        ax.minorticks_on()
        ax.grid(True, which="minor", linestyle=":", alpha=0.4)
        ax.axis("equal")
        ax.invert_yaxis()
        ax.set_title(title, pad=20, fontsize=12)
        ax.set_xlabel("X Position (m)", labelpad=10)
        ax.set_ylabel("Y Position (m)", labelpad=10)
        ax.legend(loc="upper right", framealpha=0.9)

    def __create_static_plot(
        self,
        position: Point2DWithOrientation,
        obstacles: Union[Tuple[float, float], List[Tuple[float, float]]],
        closest_obstacle: Optional[ObstacleInfo] = None,
        title: str = "",
        file_name: Optional[str] = None,
    ) -> None:
        _, ax = plt.subplots(figsize=(10, 10))
        obstacle_list = [obstacles] if isinstance(obstacles, tuple) else obstacles
        x = [obstacle[0] for obstacle in obstacle_list]
        y = [obstacle[1] for obstacle in obstacle_list]
        ax.plot(x, y, "ko", label="Obstacles", markersize=5)
        ax.plot(
            position.x,
            position.y,
            "r*",
            label=RobotConstants.YOUBOT_NAME,
            markersize=10,
        )
        plot_size = min(max(x) - min(x), max(y) - min(y)) if x else 0.5
        arrow_length = plot_size * 0.20
        dx = arrow_length * np.cos(position.yaw)
        dy = arrow_length * np.sin(position.yaw)
        ax.arrow(
            position.x,
            position.y,
            dx,
            dy,
            head_width=arrow_length * 0.4,
            head_length=arrow_length * 0.6,
            fc="r",
            ec="r",
            length_includes_head=True,
            zorder=10,
        )
        if closest_obstacle and closest_obstacle.closest_obstacle_position:
            ax.plot(
                [position.x, closest_obstacle.closest_obstacle_position[0]],
                [position.y, closest_obstacle.closest_obstacle_position[1]],
                "r--",
                linewidth=2,
                label="Path to nearest obstacle",
                alpha=0.7,
                zorder=9,
            )
        self.__setup_plot_formatting(ax, title)
        if file_name:
            plt.savefig(f"plots/{file_name}")
        plt.show()

    def start_real_time_plotting(self):
        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.is_interactive = True
        (self.robot_marker,) = self.ax.plot(
            [], [], "r*", label=RobotConstants.YOUBOT_NAME, markersize=10
        )
        (self.obstacle_dots,) = self.ax.plot(
            [], [], "ko", label="Obstacles", markersize=5
        )
        (self.ray_line,) = self.ax.plot(
            [],
            [],
            "r--",
            linewidth=2,
            label="Path to nearest obstacle",
            alpha=0.7,
            zorder=9,
        )
        self.__setup_plot_formatting(self.ax, "")
        plt.show(block=False)

    def stop_real_time_plotting(self):
        plt.ioff()
        self.is_interactive = False

    def update_plot(
        self,
        position: Point2DWithOrientation,
        obstacles: Union[Tuple[float, float], List[Tuple[float, float]]],
        closest_obstacle: Optional[ObstacleInfo] = None,
        title: str = "",
        file_name: Optional[str] = None,
    ) -> None:
        if not self.is_interactive:
            self.__create_static_plot(
                position, obstacles, closest_obstacle, title, file_name
            )
            return
        if hasattr(self, "orientation_arrow") and self.orientation_arrow:
            self.orientation_arrow.remove()
        obstacle_list = [obstacles] if isinstance(obstacles, tuple) else obstacles
        x = [obstacle[0] for obstacle in obstacle_list]
        y = [obstacle[1] for obstacle in obstacle_list]
        self.obstacle_dots.set_data(x, y)
        self.robot_marker.set_data([position.x], [position.y])
        if x and y:
            plot_size = min(max(x) - min(x), max(y) - min(y))
        else:
            plot_size = 0.5
        arrow_length = plot_size * 0.20
        dx = arrow_length * np.cos(position.yaw)
        dy = arrow_length * np.sin(position.yaw)
        self.orientation_arrow = self.ax.arrow(
            position.x,
            position.y,
            dx,
            dy,
            head_width=arrow_length * 0.2,
            head_length=arrow_length * 0.4,
            fc="r",
            ec="r",
            length_includes_head=True,
            zorder=10,
        )
        if closest_obstacle and closest_obstacle.closest_obstacle_position:
            self.ray_line.set_data(
                [position.x, closest_obstacle.closest_obstacle_position[0]],
                [position.y, closest_obstacle.closest_obstacle_position[1]],
            )
        else:
            self.ray_line.set_data([], [])
        if x:
            margin = plot_size * 0.1
            self.ax.set_xlim(min(x) - margin, max(x) + margin)
            self.ax.set_ylim(max(y) + margin, min(y) - margin)
        self.ax.set_title(title, pad=20, fontsize=12)
        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()
