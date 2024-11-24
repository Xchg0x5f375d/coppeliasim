from controllers.pattern_movement_controller import PatternMovementController
from robot.robot import Robot


def main():
    robot = Robot()
    print("\nInitial position:")
    print(robot.position)
    pattern_movement_controller = PatternMovementController(
        robot.wheel_movement_controller
    )
    print("\n=== Starting 360 degrees Environment Scan ===")
    pattern_movement_controller.perform_360_scan()
    print("\nFinal position:")
    print(robot.position)
    print(
        "Obstacles detected during scan:",
        len(robot.wheel_movement_controller.sensor_controller.obstacles),
    )
    print("\n=== Starting Forward Movement with Obstacle Detection ===")
    pattern_movement_controller.move_with_obstacle_detection(5.0, 5.0)
    print("\nFinal position:")
    print(robot.position)


if __name__ == "__main__":
    main()
