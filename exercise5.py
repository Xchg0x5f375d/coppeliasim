from controllers.pattern_movement_controller import PatternMovementController
from robot.robot import Robot


def main():
    robot = Robot()
    print("\nInitial position:")
    robot.position.print_position()
    pattern_movement_controller = PatternMovementController(
        robot.wheel_movement_controller
    )
    pattern_movement_controller.perform_360_scan()
    print("\nFinal position:")
    robot.position.print_position()


if __name__ == "__main__":
    main()
