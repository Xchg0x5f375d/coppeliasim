from abc import ABC, abstractmethod
from typing import Optional, Tuple

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
        self, name: str, operation_mode: Optional[int] = None
    ) -> Optional[Tuple[int, int]]:
        pass

    @abstractmethod
    def get_object_position(
        self,
        object_handle: int,
        reference_handle: int = -1,
        operation_mode: Optional[int] = None,
    ) -> Tuple[int, np.ndarray]:
        pass

    @abstractmethod
    def get_object_orientation(
        self,
        object_handle: int,
        reference_handle: int = -1,
        operation_mode: Optional[int] = None,
    ) -> Tuple[int, np.ndarray]:
        pass

    @abstractmethod
    def get_ping_time(self) -> int:
        pass

    @abstractmethod
    def set_object_position(
        self,
        name: str,
        position: Tuple[float, float, float],
        operation_mode: Optional[int] = None,
    ) -> None:
        pass

    @abstractmethod
    def set_joint_target_velocity(
        self, joint_handle: int, velocity: float, operation_mode: Optional[int] = None
    ) -> None:
        pass

    @abstractmethod
    def set_joint_target_position(
        self, joint_handle: int, angle: float, operation_mode: Optional[int] = None
    ) -> None:
        pass
