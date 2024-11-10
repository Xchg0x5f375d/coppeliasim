import math
import time
from typing import Any, Callable, Dict

from wheel_movement_controller import MovementDynamics, WheelMovementController


class PatternMovementController:
    def __init__(self, wheel_movement_controller: WheelMovementController):
        self.wheel_movement_controller = wheel_movement_controller

    def __print_parameters(self, pattern_name: str, params: Dict[str, Any]) -> None:
        print(f"\nExecuting {pattern_name} movement pattern...")
        print("Parameters:")
        for key, value in params.items():
            if isinstance(value, float):
                print(f"- {key}: {value:.2f}")
            else:
                print(f"- {key}: {value}")

    def __print_calculated_values(self, values: Dict[str, float]) -> None:
        print("\nCalculated values:")
        for key, value in values.items():
            print(f"- {key}: {value:.2f}")

    def _execute_timed_pattern(
        self,
        time_to_complete: float,
        velocity_calculator: Callable[[float, float], None],
        dynamics: MovementDynamics = MovementDynamics.CONSTANT,
    ) -> None:
        start_time = time.time()

        def apply_dynamics(progress: float, speed: float) -> float:
            if dynamics == MovementDynamics.CONSTANT:
                return speed
            elif dynamics == MovementDynamics.ACCELERATE:
                return speed * progress
            elif dynamics == MovementDynamics.DECELERATE:
                return speed * (1 - progress)
            elif dynamics == MovementDynamics.ACCEL_DECEL:
                if progress < 0.5:
                    return speed * (2 * progress)
                else:
                    return speed * (2 * (1 - progress))
            return speed

        while (elapsed_time := time.time() - start_time) < time_to_complete:
            progress = elapsed_time / time_to_complete
            current_speed = apply_dynamics(progress, 1.0)
            velocity_calculator(progress, current_speed)
            time.sleep(0.01)
        self.wheel_movement_controller.set_wheel_velocities(0)

    def execute_rectangular_pattern(
        self,
        length: float,
        width: float,
        speed: float,
        dynamics: MovementDynamics = MovementDynamics.CONSTANT,
    ) -> None:
        print("\nExecuting rectangular movement pattern...")
        self.wheel_movement_controller.set_wheel_velocities(0)
        sides = [length, width, length, width]
        for i, side_length in enumerate(sides):
            print(f"\nMoving along side {i+1} of rectangle ({side_length} meters)")
            self.wheel_movement_controller.move_forward(side_length, speed, dynamics)
            print("Turning 90 degrees to the right")
            self.wheel_movement_controller.turn_right(90, speed)
        self.wheel_movement_controller.set_wheel_velocities(0)
        print("\nRectangular movement pattern completed!")

    def execute_ellipsoid_pattern(
        self,
        radius_x: float,
        radius_y: float,
        speed: float,
        dynamics: MovementDynamics = MovementDynamics.CONSTANT,
    ) -> None:
        params = {
            "Semi-major axis (x)": radius_x,
            "Semi-minor axis (y)": radius_y,
            "Speed": speed,
            "Dynamics": dynamics.value,
        }
        self.__print_parameters("ellipsoid", params)
        radius = (radius_x + radius_y) / 2
        angular_velocity = speed / radius
        h = ((radius_x - radius_y) / (radius_x + radius_y)) ** 2
        perimeter = (
            math.pi
            * (radius_x + radius_y)
            * (1 + (3 * h) / (10 + math.sqrt(4 - 3 * h)))
        )
        time_to_complete = perimeter / speed
        calculated_values = {
            "Average radius": radius,
            "Angular velocity": angular_velocity,
            "Perimeter": perimeter,
            "Estimated completion time": time_to_complete,
        }
        self.__print_calculated_values(calculated_values)

        def calculate_velocities(progress: float, speed_multiplier: float) -> None:
            angle = progress * 2 * math.pi
            x = radius_x * math.cos(angle)
            y = radius_y * math.sin(angle)
            inst_radius = math.sqrt(x * x + y * y)
            inst_angular_velocity = (
                speed / inst_radius if inst_radius > 0 else angular_velocity
            ) * speed_multiplier
            velocities = self.wheel_movement_controller.calculate_path_adjusted_mecanum_velocities(
                speed * speed_multiplier,
                0,
                inst_angular_velocity,
                angle,
                path_type="ellipse",
            )
            self.wheel_movement_controller.set_wheel_velocities(velocities)

        self._execute_timed_pattern(time_to_complete, calculate_velocities, dynamics)
        print("\nEllipsoid movement pattern completed!")

    def execute_circular_pattern(
        self,
        radius: float,
        speed: float,
        num_circles: int = 1,
        clockwise: bool = True,
        dynamics: MovementDynamics = MovementDynamics.CONSTANT,
    ) -> None:
        params = {
            "Radius": radius,
            "Speed": speed,
            "Number of circles": num_circles,
            "Direction": "Clockwise" if clockwise else "Counter-clockwise",
            "Dynamics": dynamics.value,
        }
        self.__print_parameters("circular", params)
        angular_velocity = speed / radius
        if not clockwise:
            angular_velocity = -angular_velocity
        circumference = 2 * math.pi * radius
        total_distance = circumference * num_circles
        time_to_complete = total_distance / speed
        calculated_values = {
            "Angular velocity": angular_velocity,
            "Circumference": circumference,
            "Total distance": total_distance,
            "Estimated completion time": time_to_complete,
        }
        self.__print_calculated_values(calculated_values)

        def calculate_velocities(progress: float, speed_multiplier: float) -> None:
            current_progress = progress * num_circles
            angle = current_progress * 2 * math.pi
            current_angular_velocity = angular_velocity * speed_multiplier
            velocities = self.wheel_movement_controller.calculate_path_adjusted_mecanum_velocities(
                speed * speed_multiplier, 0, current_angular_velocity, angle
            )
            self.wheel_movement_controller.set_wheel_velocities(velocities)

        self._execute_timed_pattern(time_to_complete, calculate_velocities, dynamics)
        print(f"\nCircular movement pattern completed {num_circles} time(s)!")

    def execute_figure_eight_pattern(
        self,
        radius: float,
        speed: float,
        dynamics: MovementDynamics = MovementDynamics.CONSTANT,
    ) -> None:
        params = {
            "Radius": radius,
            "Speed": speed,
            "Dynamics": dynamics.value,
        }
        self.__print_parameters("figure-eight", params)
        circumference = 2 * math.pi * radius
        time_per_circle = circumference / speed
        time_to_complete = time_per_circle * 2  # Two circles

        def calculate_velocities(progress: float, speed_multiplier: float) -> None:
            in_first_circle = progress < 0.5
            circle_progress = (progress * 2) % 1
            angle = circle_progress * 2 * math.pi
            if not in_first_circle:
                angle = -angle
            angular_velocity = (speed / radius) * (1 if in_first_circle else -1)
            velocities = self.wheel_movement_controller.calculate_path_adjusted_mecanum_velocities(
                speed * speed_multiplier, 0, angular_velocity * speed_multiplier, angle
            )
            self.wheel_movement_controller.set_wheel_velocities(velocities)

        self._execute_timed_pattern(time_to_complete, calculate_velocities, dynamics)
        print("\nFigure-eight pattern completed!")

    def execute_spiral_pattern(
        self,
        start_radius: float,
        end_radius: float,
        speed: float,
        num_revolutions: int = 2,
        clockwise: bool = True,
        dynamics: MovementDynamics = MovementDynamics.CONSTANT,
    ) -> None:
        params = {
            "Start radius": start_radius,
            "End radius": end_radius,
            "Speed": speed,
            "Number of revolutions": num_revolutions,
            "Direction": "Clockwise" if clockwise else "Counter-clockwise",
            "Dynamics": dynamics.value,
        }
        self.__print_parameters("spiral", params)
        radius_change_per_revolution = (end_radius - start_radius) / num_revolutions
        avg_radius = (start_radius + end_radius) / 2
        avg_circumference = 2 * math.pi * avg_radius
        total_distance = avg_circumference * num_revolutions
        time_to_complete = total_distance / speed
        calculated_values = {
            "Average radius": avg_radius,
            "Radius change per revolution": radius_change_per_revolution,
            "Approximate total distance": total_distance,
            "Estimated completion time": time_to_complete,
        }
        self.__print_calculated_values(calculated_values)

        def calculate_velocities(progress: float, speed_multiplier: float) -> None:
            angle = progress * num_revolutions * 2 * math.pi
            if not clockwise:
                angle = -angle
            current_radius = start_radius + (progress * (end_radius - start_radius))
            inst_angular_velocity = (speed / current_radius) * speed_multiplier
            if not clockwise:
                inst_angular_velocity = -inst_angular_velocity
            velocities = self.wheel_movement_controller.calculate_path_adjusted_mecanum_velocities(
                speed * speed_multiplier, 0, inst_angular_velocity, angle
            )
            self.wheel_movement_controller.set_wheel_velocities(velocities)

        def apply_dynamics(progress: float) -> float:
            if dynamics == MovementDynamics.CONSTANT:
                return 1.0
            elif dynamics == MovementDynamics.ACCELERATE:
                return progress
            elif dynamics == MovementDynamics.DECELERATE:
                return 1.0 - progress
            elif dynamics == MovementDynamics.ACCEL_DECEL:
                if progress < 0.5:
                    return 2 * progress
                else:
                    return 2 * (1 - progress)
            return 1.0

        start_time = time.time()
        self.wheel_movement_controller.set_wheel_velocities(0)
        while (elapsed_time := time.time() - start_time) < time_to_complete:
            progress = elapsed_time / time_to_complete
            speed_multiplier = apply_dynamics(progress)
            calculate_velocities(progress, speed_multiplier)
            time.sleep(0.01)
        self.wheel_movement_controller.set_wheel_velocities(0)
        print("\nSpiral movement pattern completed!")

    def execute_star_pattern(
        self,
        radius: float,
        points: int,
        speed: float,
        dynamics: MovementDynamics = MovementDynamics.CONSTANT,
    ) -> None:
        params = {
            "Radius": radius,
            "Number of points": points,
            "Speed": speed,
            "Dynamics": dynamics.value,
        }
        self.__print_parameters("star", params)
        angle_between_points = 360 / points
        for point in range(points):
            print(f"\nDrawing point {point + 1} of {points}:")
            print(f"- Moving outward {radius} meters...")
            self.wheel_movement_controller.move_forward(radius, speed, dynamics)
            print(f"- Moving back to center {radius} meters...")
            self.wheel_movement_controller.move_forward(radius, -speed, dynamics)
            if point < points - 1:
                print(
                    f"- Rotating {angle_between_points:.2f} degrees for next point..."
                )
                self.wheel_movement_controller.turn_right(angle_between_points, speed)
        print("\nStar pattern completed!")

    def execute_zigzag_pattern(
        self,
        length: float,
        width: float,
        num_zigzags: int,
        speed: float,
        dynamics: MovementDynamics = MovementDynamics.CONSTANT,
    ) -> None:
        params = {
            "Length": length,
            "Width": width,
            "Number of zigzags": num_zigzags,
            "Speed": speed,
            "Dynamics": dynamics.value,
        }
        self.__print_parameters("zigzag", params)
        segment_length = length / num_zigzags
        total_distance = length + (width * num_zigzags)
        estimated_time = total_distance / speed
        calculated_values = {
            "Segment length": segment_length,
            "Total distance": total_distance,
            "Estimated completion time": estimated_time,
        }
        self.__print_calculated_values(calculated_values)
        self.wheel_movement_controller.set_wheel_velocities(0)
        for i in range(num_zigzags):
            print(f"\nExecuting zigzag segment {i + 1} of {num_zigzags}:")
            print(f"- Moving forward {segment_length:.2f} meters...")
            self.wheel_movement_controller.move_forward(segment_length, speed, dynamics)
            if i < num_zigzags - 1:
                if i % 2 == 0:
                    print("- Turning right 90 degrees...")
                    self.wheel_movement_controller.turn_right(90, speed)
                    print(f"- Moving across {width:.2f} meters...")
                    self.wheel_movement_controller.move_forward(width, speed, dynamics)
                    print("- Turning left 90 degrees...")
                    self.wheel_movement_controller.turn_right(-90, speed)
                else:
                    print("- Turning left 90 degrees...")
                    self.wheel_movement_controller.turn_right(-90, speed)
                    print(f"- Moving across {width:.2f} meters...")
                    self.wheel_movement_controller.move_forward(width, speed, dynamics)
                    print("- Turning right 90 degrees...")
                    self.wheel_movement_controller.turn_right(90, speed)
        print("\nZigzag pattern completed!")
        print(
            f"Completed {num_zigzags} zigzags over {length:.2f} meters with {width:.2f} meter width"
        )
