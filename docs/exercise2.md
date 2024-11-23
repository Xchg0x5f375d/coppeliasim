# Exercise 2: Basic Robot Movement and Control

## Overview

This exercise introduces fundamental robot movement and control operations using the YouBot platform in CoppeliaSim. It
demonstrates basic movement patterns and arm manipulation capabilities.

![Exercise 2 Demo](/docs/assets/exercise2.gif)

## Key Features

### 1. Basic Movement Controls

- Forward/backward movement with constant velocity
- Controlled rotation (90-degree turns)
- Complete stop functionality
- Precise distance-based movement

### 2. Pattern Movement

- Square pattern execution (1m x 1m)
- Automated sequence of movements:
    - Forward movement
    - 90-degree turns
    - Pattern completion verification

### 3. Arm Manipulation

- Control of 5 arm joints
- Sequential arm movements
- Basic positioning capabilities

## Usage

1. Start CoppeliaSim
2. Load scene: `scenes/movement.ttt`
3. Run: `python exercise2.py`

## Expected Behavior

1. Robot executes a 1x1 meter square pattern
2. Performs a series of arm movements
3. Provides movement feedback in console

## Results

Successfully implemented all required movement and control functionalities:

- ✅ Velocity control
- ✅ Square pattern movement
- ✅ Arm joint manipulation
- ✅ Precise movement control
