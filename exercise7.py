from robot.robot import Robot


def main():
    robot = Robot()
    robot.path_planning_controller.plan_and_execute_path(
        script_name="end", function_name="findPath"
    )


if __name__ == "__main__":
    main()
