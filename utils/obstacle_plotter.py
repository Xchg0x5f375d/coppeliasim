from datetime import datetime
from typing import Callable, List, Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np

from constants import RobotConstants
from models.obstacle_info import ObstacleInfo
from models.point2d_with_orientation import Point2DWithOrientation


class ObstaclePlotter:
    def __init__(self):
        self.fig = None
        self.ax = None

    def __setup_plot_formatting(self, title: str) -> None:
        self.ax.grid(True, linestyle="--", alpha=0.7)
        self.ax.minorticks_on()
        self.ax.grid(True, which="minor", linestyle=":", alpha=0.4)
        self.ax.set_aspect("equal")
        self.ax.invert_yaxis()
        self.ax.set_title(title, pad=20, fontsize=12)
        self.ax.set_xlabel("X Position (m)", labelpad=10)
        self.ax.set_ylabel("Y Position (m)", labelpad=10)
        self.ax.legend(loc="upper right", framealpha=0.9)

    def __draw_orientation_arrow(
        self, position: Point2DWithOrientation, plot_size: float, plot_width: float
    ) -> None:
        marker_size = 10
        points_to_pixels = self.fig.dpi / 72
        marker_radius = (
            (marker_size * points_to_pixels) / self.fig.dpi * plot_size * 0.05
        )
        start_x = position.x + marker_radius * np.cos(position.yaw)
        start_y = position.y + marker_radius * np.sin(position.yaw)
        arrow_length = plot_size * 0.08
        self.ax.arrow(
            start_x,
            start_y,
            arrow_length * np.cos(position.yaw),
            arrow_length * np.sin(position.yaw),
            head_width=plot_width * 0.04,
            head_length=plot_size * 0.06,
            fc="r",
            ec="r",
            length_includes_head=True,
            zorder=10,
        )

    def plot_obstacles(
        self,
        position: Point2DWithOrientation,
        obstacles: Union[Tuple[float, float], List[Tuple[float, float]]],
        title: str = "",
        save_path: Optional[str] = f"{datetime.now().isoformat()}.png",
        callbacks: Optional[List[Union[Callable[[plt.Axes], None], Callable]]] = None,
    ) -> None:
        self.fig = plt.figure(figsize=(10, 10))
        self.ax = self.fig.gca()
        obstacle_list = [obstacles] if isinstance(obstacles, tuple) else obstacles
        x = [obstacle[0] for obstacle in obstacle_list]
        y = [obstacle[1] for obstacle in obstacle_list]
        self.ax.plot(x, y, "ko", label="Obstacles", markersize=5)
        self.ax.plot(
            position.x,
            position.y,
            "r*",
            label=RobotConstants.YOUBOT_NAME,
            markersize=10,
        )
        x_min, x_max = min(x + [position.x]), max(x + [position.x])
        y_min, y_max = min(y + [position.y]), max(y + [position.y])
        plot_width = x_max - x_min
        plot_height = y_max - y_min
        plot_size = min(plot_width, plot_height)
        self.__draw_orientation_arrow(position, plot_size, plot_width)
        self.__setup_plot_formatting(title)
        if callbacks:
            for callback in callbacks:
                callback(self.ax)
        plt.tight_layout()
        if save_path:
            self.fig.savefig(f"plots/{save_path}")
        plt.show()

    def plot_ray_trace(
        self, position: Point2DWithOrientation, target_obstacle: ObstacleInfo
    ) -> None:
        if self.ax is None:
            raise RuntimeError("Must call plot_obstacles before plot_ray_trace")
        self.ax.plot(
            [position.x, target_obstacle.closest_obstacle[0]],
            [position.y, target_obstacle.closest_obstacle[1]],
            "r--",
            alpha=0.7,
        )
