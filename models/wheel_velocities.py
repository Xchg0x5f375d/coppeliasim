from dataclasses import dataclass

import numpy as np


@dataclass
class WheelVelocities:
    front_left: float
    rear_left: float
    rear_right: float
    front_right: float

    def to_array(self) -> np.ndarray:
        return np.array(
            [self.front_left, self.rear_left, self.rear_right, self.front_right]
        )
