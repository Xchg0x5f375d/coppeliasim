# Exercise 7: Path following paths generated from the simulator

## Overview

This exercise implements advanced path planning and control capabilities for a simulated YouBot robot in CoppeliaSim,
utilizing the Open Motion Planning Library (OMPL) for path generation and a refined control system for accurate path
following. The robot can now navigate complex environments, dynamically compute collision-free paths, and execute them
with precision, while also demonstrating the ability to interact with the simulation environment through remote script
function calls.

![Exercise 7 Demo](/docs/assets/exercise7.gif)

## Control Capabilities

### Path Planning Features

- **Algorithm Selection:** Choose from a range of OMPL planners to suit different scenarios
- **On-Demand Path Generation:** Compute paths dynamically based on the robot's current state and desired goal
- **Path Data Access:** Retrieve generated path information from CoppeliaSim for further processing or analysis

### Movement and Navigation

- **Accurate Path Execution:** Follow generated paths with high precision
- **Dynamic Adjustments:**  Continuously adjust movement based on real-time feedback to maintain accuracy
- **Controlled Stops:** Bring the robot to a controlled stop when necessary

## Path Following Behavior

### Planning Process

1. **Planner Selection:** The user selects an OMPL path planning algorithm
2. **Path Computation:**  The `PathPlanningController` calls a Lua function in CoppeliaSim (using
   `call_script_function`) to compute a path with the chosen planner
3. **Path Retrieval:** The computed path data is retrieved and stored

### Execution Process

1. **Orientation Alignment:** The robot aligns itself towards the first point on the path using `turn_towards_goal`
2. **Point-to-Point Movement:** The robot iterates through the points on the path, moving towards each using
   `move_towards_point`
3. **Dynamic Adjustment:**  The `WheelMovementController` continuously adjusts wheel velocities using `move_and_adjust`
   to maintain accuracy, based on the angle to the goal, direction of the turn and distance to the point
4. **Goal Reached:** The robot stops when it reaches the final point on the path

## Example Operations

### Path Planning and Execution

```python
path_planning_controller.plan_and_execute_path("end", "findPath")
```

## Usage

1. Start CoppeliaSim
2. Load scene: `scenes/movement.ttt`
3. Run: `python exercise7.py`

## Results

Successfully implemented:

- ✅ Remote Script Function Calling: Seamless communication between Python and Lua in CoppeliaSim
- ✅ OMPL-Based Path Planning: Dynamic path generation using various OMPL algorithms
- ✅ Precise Path Following: Accurate execution of computed paths
- ✅ Enhanced Robot Control: Fine-grained control over robot movements
- ✅ Modular Design: Well-structured and maintainable code through a modular architecture
- ✅ Path following: Robot follows generated path using implemented functions
