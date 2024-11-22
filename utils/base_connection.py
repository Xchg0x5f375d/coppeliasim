from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

import numpy as np


class BaseConnection(ABC):
    @abstractmethod
    def connect(self) -> bool:
        pass

    @abstractmethod
    def disconnect(self) -> bool:
        pass

    @abstractmethod
    def start_simulation(self) -> bool:
        pass

    @abstractmethod
    def stop_simulation(self) -> bool:
        pass

    @abstractmethod
    def get_object_handle(
        self, name: str, operation_mode: int
    ) -> Optional[Tuple[int, int]]:
        pass

    @abstractmethod
    def get_object_position(
        self, object_handle: int, reference_handle: int, operation_mode: int
    ) -> Tuple[int, np.ndarray]:
        pass

    @abstractmethod
    def get_object_orientation(
        self, object_handle: int, reference_handle: int, operation_mode: int
    ) -> Tuple[int, np.ndarray]:
        pass

    @abstractmethod
    def get_ping_time(self) -> int:
        pass

    @abstractmethod
    def set_object_position(
        self, name: str, position: Tuple[float, float, float], operation_mode: int
    ) -> None:
        pass

    @abstractmethod
    def set_joint_target_velocity(
        self, joint_handle: int, velocity: float, operation_mode: int
    ) -> None:
        pass

    @abstractmethod
    def set_joint_target_position(
        self, joint_handle: int, angle: float, operation_mode: int
    ) -> None:
        pass

    @abstractmethod
    def set_integer_signal(self, signal: Tuple[str, int], operation_mode: int) -> int:
        pass

    @abstractmethod
    def read_vision_sensor(
        self, sensor_handle: Optional[Tuple[int, int]], operation_mode: int
    ) -> Tuple[int, bool, List[List[float]]]:
        pass
