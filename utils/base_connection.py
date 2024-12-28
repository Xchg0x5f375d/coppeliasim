from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, Union

import numpy as np

from models.vision_sensor_data import VisionSensorData
from utils.script_function_result import ScriptFunctionResult


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
    def load_scene(self, scene_file: str) -> bool:
        pass

    @abstractmethod
    def get_object_handle(
        self, name: str, operation_mode: Optional[int] = None
    ) -> Optional[Tuple[int, int]]:
        pass

    @abstractmethod
    def get_object_position(
        self,
        object_handle: Union[int, str],
        reference_handle: int = -1,
        operation_mode: Optional[int] = None,
    ) -> Tuple[int, np.ndarray]:
        pass

    @abstractmethod
    def get_object_orientation(
        self,
        object_handle: Union[int, str],
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

    @abstractmethod
    def set_float_signal(
        self, signal: Tuple[str, float], operation_mode: Optional[int] = None
    ) -> int:
        pass

    @abstractmethod
    def set_integer_signal(
        self, signal: Tuple[str, int], operation_mode: Optional[int] = None
    ) -> int:
        pass

    @abstractmethod
    def read_vision_sensor(
        self,
        sensor_handle: Optional[Tuple[int, int]],
        operation_mode: Optional[int] = None,
    ) -> Tuple[int, bool, List[List[float]]]:
        pass

    @abstractmethod
    def call_script_function(
        self,
        script_description: str,
        function_name: str,
        options: Optional[int] = None,
        input_ints: Optional[List[int]] = None,
        input_floats: Optional[List[float]] = None,
        input_strings: Optional[List[str]] = None,
        input_buffer: List[bytearray] = bytearray(),
        operation_mode: Optional[int] = None,
    ) -> ScriptFunctionResult:
        pass

    @abstractmethod
    def get_vision_sensor_image(
        self,
        object_handle: Union[int, str],
        options: int = 0,
        operation_mode: Optional[int] = None,
    ) -> Optional[VisionSensorData]:
        pass

    @abstractmethod
    def auxiliary_console_print(
        self,
        title: str,
        message: str,
        max_lines: int = 100,
        mode: int = 6,
        position: Optional[Tuple[int, int]] = (100, 100),
        size: Optional[Tuple[int, int]] = (800, 600),
        text_color: Optional[Tuple[int, int, int]] = (0, 0, 0),
        background_color: Tuple[int, int, int] = (255, 255, 255),
        operation_mode: Optional[int] = None,
    ) -> int:
        pass
