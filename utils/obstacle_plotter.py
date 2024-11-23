from typing import Callable, List, Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np

from constants import RobotConstants
from models.obstacle_info import ObstacleInfo


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
    def __plot_robot_orientation(position: Tuple[float, float]) -> None:
        arrow_length = 0.1
        plt.quiver(
            position[0],
            position[1],
            arrow_length * np.cos(position[2]),
            arrow_length * np.sin(position[2]),
            color="r",
            scale=10.0,
            scale_units="xy",
            angles="xy",
            width=0.005,
            headwidth=2,
            headlength=3,
            headaxislength=2,
            zorder=5,
        )

    @staticmethod
    def plot_obstacles(
        position: Tuple[float, float],
        obstacles: Union[Tuple[float, float], List[Tuple[float, float]]],
        title: str = "",
        save_path: Optional[str] = "image.png",
        callbacks: Optional[List[Union[Callable[[plt.Axes], None], Callable]]] = None,
    ) -> None:
        obstacle_list = [obstacles] if isinstance(obstacles, tuple) else obstacles
        x = [obs[0] for obs in obstacle_list]
        y = [obs[1] for obs in obstacle_list]
        plt.figure(figsize=(10, 10))
        ax = plt.gca()
        plt.plot(x, y, "ko", label="Obstacles", markersize=5)
        plt.plot(
            position[0],
            position[1],
            "r*",
            label=RobotConstants.YOUBOT_NAME,
            markersize=10,
        )
        ObstaclePlotter.__plot_robot_orientation(position)
        ObstaclePlotter.__setup_plot_formatting(title)
        if callbacks:
            for callback in callbacks:
                callback(ax)
        plt.tight_layout()
        if save_path:
            plt.savefig(f"docs/{save_path}")
        plt.show()

    @staticmethod
    def plot_ray_trace(
        position: Tuple[float, float], target_obstacle: ObstacleInfo
    ) -> None:
        plt.plot(
            [position[0], target_obstacle.closest_obstacle[0]],
            [position[1], target_obstacle.closest_obstacle[1]],
            "r--",
            alpha=0.7,
        )
