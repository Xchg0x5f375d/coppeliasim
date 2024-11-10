from pattern_movement_controller import PatternMovementController
from robot import Robot
from wheel_movement_controller import MovementDynamics, WheelMovementController


def test_movement_patterns(
    pattern_movement_controller: PatternMovementController,
) -> None:
    print("\nExecuting Rectangle Path - Constant Speed")
    pattern_movement_controller.execute_rectangular_pattern(
        length=2.0,
        width=1.0,
        speed=5.0,
    )
    print("\nExecuting Rectangle Path - With Acceleration/Deceleration")
    pattern_movement_controller.execute_rectangular_pattern(
        length=2.0, width=1.0, speed=5.0, dynamics=MovementDynamics.ACCEL_DECEL
    )
    print("\nExecuting Circular Path - Constant Speed")
    pattern_movement_controller.execute_circular_pattern(
        radius=1.0, speed=0.5, num_circles=2
    )
    print("\nExecuting Circular Path - Counter-clockwise")
    pattern_movement_controller.execute_circular_pattern(
        radius=1.2, speed=0.5, clockwise=False
    )


def test_different_velocities(
    pattern_movement_controller: PatternMovementController,
) -> None:
    print("\Executing Forward Movement with Acceleration/Deceleration:")
    pattern_movement_controller.wheel_movement_controller.move_forward(
        distance=5.0, speed=15.0, dynamics=MovementDynamics.ACCEL_DECEL
    )
    pattern_movement_controller.wheel_movement_controller.move_forward(
        distance=5.0, speed=-15.0, dynamics=MovementDynamics.ACCEL_DECEL
    )
    print("\Executing Backward Movement with Acceleration/Deceleration:")


def test_complex_trajectories(
    pattern_movement_controller: PatternMovementController,
) -> None:
    print("\nExecuting Circular Pattern - Constant Speed:")
    pattern_movement_controller.execute_circular_pattern(
        radius=1.0, speed=0.5, num_circles=2, dynamics=MovementDynamics.CONSTANT
    )
    print("\nExecuting Circular Pattern - With Acceleration/Deceleration:")
    pattern_movement_controller.execute_circular_pattern(
        radius=1.0, speed=0.5, num_circles=2, dynamics=MovementDynamics.ACCEL_DECEL
    )
    print("\nExecuting Star Pattern - Constant Speed:")
    pattern_movement_controller.execute_star_pattern(
        radius=1.0, points=5, speed=15.0, dynamics=MovementDynamics.CONSTANT
    )
    print("\nExecuting Star Pattern - With Acceleration:")
    pattern_movement_controller.execute_star_pattern(
        radius=1.0, points=5, speed=15.0, dynamics=MovementDynamics.ACCELERATE
    )
    print("\nExecuting Zigzag Pattern - Constant Speed:")
    pattern_movement_controller.execute_zigzag_pattern(
        length=4.0,
        width=1.0,
        num_zigzags=3,
        speed=10.0,
        dynamics=MovementDynamics.CONSTANT,
    )
    print("\nExecuting Zigzag Pattern - With Deceleration:")
    pattern_movement_controller.execute_zigzag_pattern(
        length=4.0,
        width=1.0,
        num_zigzags=3,
        speed=10.0,
        dynamics=MovementDynamics.DECELERATE,
    )
    print("\nExecuting Rectangular Pattern - Constant Speed:")
    pattern_movement_controller.execute_rectangular_pattern(
        length=2.0, width=1.0, speed=2.0, dynamics=MovementDynamics.CONSTANT
    )
    print("\nExecuting Rectangular Pattern - With Acceleration/Deceleration:")
    pattern_movement_controller.execute_rectangular_pattern(
        length=2.0, width=1.0, speed=2.0, dynamics=MovementDynamics.ACCEL_DECEL
    )
    print("\nExecuting Figure-Eight Pattern - Constant Speed:")
    pattern_movement_controller.execute_figure_eight_pattern(
        radius=1.0, speed=0.5, dynamics=MovementDynamics.CONSTANT
    )
    print("\nExecuting Figure-Eight Pattern - With Acceleration:")
    pattern_movement_controller.execute_figure_eight_pattern(
        radius=1.0, speed=0.5, dynamics=MovementDynamics.ACCELERATE
    )
    print("\nExecuting Spiral Pattern - Constant Speed:")
    pattern_movement_controller.execute_spiral_pattern(
        start_radius=0.5,
        end_radius=2.0,
        speed=2.0,
        num_revolutions=2,
        dynamics=MovementDynamics.CONSTANT,
    )
    print("\nExecuting Spiral Pattern - With Acceleration/Deceleration:")
    pattern_movement_controller.execute_spiral_pattern(
        start_radius=0.5,
        end_radius=2.0,
        speed=2.0,
        num_revolutions=2,
        dynamics=MovementDynamics.ACCEL_DECEL,
    )


def main():
    robot = Robot()
    wheel_movement_controller = WheelMovementController(
        robot.vrep_connection, robot.wheel_joints
    )
    pattern_movement_controller = PatternMovementController(wheel_movement_controller)
    test_movement_patterns(pattern_movement_controller)
    test_different_velocities(pattern_movement_controller)
    test_complex_trajectories(pattern_movement_controller)


if __name__ == "__main__":
    main()
