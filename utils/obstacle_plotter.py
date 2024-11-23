from typing import Callable, List, Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np

from constants import RobotConstants
from models.obstacle_info import ObstacleInfo
from models.point2d_with_orientation import Point2DWithOrientation


class ObstaclePlotter:
    @staticmethod
    def __setup_plot_formatting(title: str) -> None:
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.minorticks_on()
        plt.grid(True, which="minor", linestyle=":", alpha=0.4)
        plt.axis("equal")
        plt.gca().invert_yaxis()
        plt.title(title, pad=20, fontsize=12)
        plt.xlabel("X Position (m)", labelpad=10)
        plt.ylabel("Y Position (m)", labelpad=10)
        plt.legend(loc="upper right", framealpha=0.9)

    @staticmethod
    def plot_obstacles(
        position: Point2DWithOrientation,
        obstacles: Union[Tuple[float, float], List[Tuple[float, float]]],
        title: str = "",
        save_path: Optional[str] = "image.png",
        callbacks: Optional[List[Union[Callable[[plt.Axes], None], Callable]]] = None,
    ) -> None:
        obstacle_list = [obstacles] if isinstance(obstacles, tuple) else obstacles
        x = [obstacle[0] for obstacle in obstacle_list]
        y = [obstacle[1] for obstacle in obstacle_list]
        plt.figure(figsize=(10, 10))
        ax = plt.gca()
        plt.plot(x, y, "ko", label="Obstacles", markersize=5)
        plt.plot(
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
        arrow_length = plot_size * 0.25
        plt.arrow(
            position.x,
            position.y,
            arrow_length * np.cos(position.yaw),
            arrow_length * np.sin(position.yaw),
            head_width=plot_width * 0.08,
            head_length=plot_size * 0.12,
            fc="r",
            ec="r",
            length_includes_head=True,
            zorder=10,
        )
        ObstaclePlotter.__setup_plot_formatting(title)
        if callbacks:
            for callback in callbacks:
                callback(ax)
        plt.tight_layout()
        if save_path:
            plt.savefig(f"plots/{save_path}")
        plt.show()

    @staticmethod
    def plot_ray_trace(
        position: Point2DWithOrientation, target_obstacle: ObstacleInfo
    ) -> None:
        plt.plot(
            [position.x, target_obstacle.closest_obstacle[0]],
            [position.y, target_obstacle.closest_obstacle[1]],
            "r--",
            alpha=0.7,
        )
