# Autonomous Robotics Control & Simulation

## CoppeliaSim Implementation Framework

This repository contains different robotics exercises implemented in CoppeliaSim (formerly V-REP). Each exercise is
maintained in a separate file for better organization and clarity.

## 📚 Exercises

- `exercise2.py` - Basic robot movement and control
- `exercise3.py` - Robot trajectories and movement dynamics
- `exercise4.py` - Odometry of the mobile robots
- `exercise5.py` - Obstacle detection with Hokuyo sensor laser beams
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
│   └── robot_constants.py
├── controllers/
│   ├── __init__.py
│   ├── arm_movement_controller.py
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
│   │   └── exercise8.png
│   ├── exercise2.md
│   ├── exercise3.md
│   ├── exercise4.md
│   └── exercise5.md
│   └── exercise8.md
├── models/
│   ├── __init__.py
│   ├── movement_dynamics.py
│   ├── obstacle_detection_result.py
│   ├── obstacle_info.py
│   ├── path_types.py
│   ├── point2d_with_orientation.py
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
│   ├── obstacle_plotter.py
│   ├── remoteApi.dll
│   ├── vrep.py
│   ├── vrep_connection.py
│   └── vrepConst.py
├── exercise2.py
├── exercise3.py
├── exercise4.py
├── exercise5.py
├── exercise8.py
├── README.md
├── requirements.txxt
└── .gitignore
```
