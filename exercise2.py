import math

from controllers.pattern_movement_controller import PatternMovementController
from robot.robot import Robot


def main():
    robot = Robot()
    pattern_movement_controller = PatternMovementController(
        robot.wheel_movement_controller
    )
    pattern_movement_controller.execute_rectangular_pattern(
        length=1.0, width=1.0, speed=5.0
    )
    arm_movements = [(2, i * math.pi / 8) for i in range(4)]
    robot.arm_movement_controller.move_arm(arm_movements)


if __name__ == "__main__":
    main()
