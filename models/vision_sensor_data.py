from dataclasses import dataclass
from typing import List

from utils import vrep


@dataclass
class VisionSensorData:
    error_code: int
    resolution: List[int]
    image: List[int]

    @property
    def success(self) -> bool:
        return self.error_code == vrep.simx_return_ok

    @staticmethod
    def empty() -> "VisionSensorData":
        return VisionSensorData(error_code=-1, resolution=[], image=[])
