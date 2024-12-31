# Autonomous Robotics Control & Simulation

## CoppeliaSim Implementation Framework

This repository contains different robotics exercises implemented in CoppeliaSim (formerly V-REP). Each exercise is
maintained in a separate file for better organization and clarity.

## 📚 Exercises

- `exercise2.py` - Basic robot movement and control
- `exercise3.py` - Robot trajectories and movement dynamics
- `exercise4.py` - Odometry of the mobile robots
- `exercise5.py` - Obstacle detection with Hokuyo sensor laser beams
- `exercise7.py` - Path following paths generated from the simulator
- `exercise8.py` - Color Blob Detection with Vision Sensor

## 🛠️ Prerequisites

- Python 3.x
- CoppeliaSim EDU/PRO V4.x
- Required Python packages:
  `numpy matplotlib opencv-python pillow`

## 🚀 Getting Started

1. Clone the repository:
   `git clone https://github.com/Xchg0x5f375d/coppeliasim`

2. Start CoppeliaSim simulator

3. Load the corresponding scene file:
    - Located in `scenes/` directory
    - Match the scene with current exercise

4. Run the desired exercise file:
   `python exercise<number>.py`

## 📁 Project Structure

```
coppeliasim/
├── constants/
│   ├── __init__.py
│   ├── path_constants.py
│   └── robot_constants.py
├── controllers/
│   ├── __init__.py
│   ├── arm_movement_controller.py
│   ├── image_controller.py
│   ├── path_planning_controller.py
│   ├── pattern_movement_controller.py
│   ├── sensor_controller.py
│   └── wheel_movement_controller.py
├── docs/
│   ├── assets/
│   │   ├── exercise2.gif
│   │   ├── exercise3.gif
│   │   ├── exercise4.gif
│   │   ├── exercise4.png
│   │   ├── exercise5.gif
│   │   ├── exercise7.gif
│   │   └── exercise8.png
│   ├── exercise2.md
│   ├── exercise3.md
│   ├── exercise4.md
│   ├── exercise5.md
│   ├── exercise7.md
│   └── exercise8.md
├── models/
│   ├── __init__.py
│   ├── movement_dynamics.py
│   ├── obstacle_detection_result.py
│   ├── obstacle_info.py
│   ├── path_types.py
│   ├── point2d_with_orientation.py
│   ├── vision_sensor_data.py
│   └── wheel_velocities.py
├── plots/
│   └── exercise5/
│       ├── exercise5.png
├── robot/
│   ├── __init__.py
│   ├── robot.py
│   └── robot_position.py
├── scenes/
│   ├── movement.ttt
    └── colors.ttt
├── utils/
│   ├── __init__.py
│   ├── base_connection.py
│   ├── linalg_utils.py
│   ├── obstacle_plotter.py
│   ├── remoteApi.dll
│   ├── script_function_result.py
│   ├── vrep.py
│   ├── vrep_connection.py
│   └── vrepConst.py
├── .gitignore
├── Dockerfile
├── README.md
├── exercise2.py
├── exercise3.py
├── exercise4.py
├── exercise5.py
├── exercise7.py
├── exercise8.py
└── requirements.txxt
```
