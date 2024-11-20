from controllers.pattern_movement_controller import PatternMovementController
from robot.robot import Robot


def main():
    robot = Robot()
    pattern_movement_controller = PatternMovementController(
        robot.wheel_movement_controller
    )
    obstacles = pattern_movement_controller.scan_and_move()
    robot.sensor_controller.visualize_obstacles(obstacles)


if __name__ == "__main__":
    main()
