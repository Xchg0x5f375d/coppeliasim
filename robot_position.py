class RobotPosition:
    def __init__(self):
        self.x: float = -4.700
        self.y: float = 0.200
        self.yaw: float = 0.0957

    def to_position_tuple(self) -> tuple[float, float, float]:
        return (self.x, self.y, self.yaw)
