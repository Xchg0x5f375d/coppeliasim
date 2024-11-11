class RobotPosition:
    def __init__(self, x: float = -4.700, y: float = 0.200, yaw: float = 0.0957):
        self.x = x
        self.y = y
        self.yaw = yaw

    def to_position_tuple(self) -> tuple[float, float, float]:
        return (self.x, self.y, self.yaw)
