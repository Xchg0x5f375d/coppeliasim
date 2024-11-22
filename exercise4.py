from robot.robot import Robot


def main():
    robot = Robot()
    print("\nInitial position:")
    print(robot.position)
    print("\nMoving forward 1 meter...")
    robot.wheel_movement_controller.move_forward(distance=1.0, speed=5.0)
    print(robot.position)
    print("\nTurning right 90 degrees...")
    robot.wheel_movement_controller.turn_right(degree=90, speed=5.0)
    print(robot.position)
    print("\nMoving forward 1 meter...")
    robot.wheel_movement_controller.move_forward(distance=1.0, speed=5.0)
    print(robot.position)
    print("\nTurning right 90 degrees...")
    robot.wheel_movement_controller.turn_right(degree=90, speed=5.0)
    print(robot.position)


if __name__ == "__main__":
    main()
