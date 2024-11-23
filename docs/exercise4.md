# Exercise 4: Robot Odometry and Position Tracking

## Overview

This exercise implements position tracking and odometry calculations for the YouBot platform, enabling accurate
monitoring of the robot's position and orientation during movement.

![Exercise 4 Demo](/docs/assets/exercise4.gif)

## Key Features

### 1. Position Tracking

- Global position monitoring
- Local coordinate tracking
- Real-time orientation updates
- High-precision measurements (5 decimal places)

### 2. Odometry System

- Distance-based position updates
- Angle-based orientation tracking
- Continuous position estimation
- Movement validation

### 3. Position Reporting

- Global coordinates [X, Y, θ]
- Local coordinates tracking
- Orientation in radians
- Real-time position updates

## Position Tracking Demo

### Movement Sequence

1. Forward Movement (1m)
    - Initial: (-4.70013, 0.20117, -1.57093)
    - Final: (-4.70026, -0.79883, -1.57093)

2. Right Turn (90°)
    - Before: (-4.70013, -0.8, -1.57093)
    - After: (-4.70013, -0.8, -0.00013)

3. Forward Movement (1m)
    - Before: (-4.70013, -0.8, -0.00013)
    - After: (-3.70013, -0.80013, -0.00013)

4. Right Turn (90°)
    - Before: (-3.70013, -0.80013, -0.00013)
    - After: (-3.70013, -0.80013, 1.57066)

## Usage

1. Start CoppeliaSim
2. Load scene: `scenes/movement.ttt`
3. Run: `python exercise4.py`

## Results

Successfully implemented:

- ✅ Accurate position tracking
- ✅ Precise orientation monitoring
- ✅ Real-time coordinate updates
- ✅ Movement validation
- ✅ Odometry calculations
