# Exercise 8: Color Blob Detection with Vision Sensor

## Overview

This exercise focuses on utilizing a simulated RGB-D camera in CoppeliaSim to detect and track colored blobs. It
implements color filtering and blob detection using OpenCV to identify red and blue objects within the robot's field of
view.

![Exercise 8 Demo](/docs/assets/exercise8.png)

## Key Features

### 1. RGB-D Sensor Simulation

- Leverages CoppeliaSim's vision sensor for RGB and depth data acquisition
- Captures images from a simulated RGB camera mounted on a YouBot robot

### 2. Color-Based Object Detection

- Implements color filtering using OpenCV's inRange() function
- Defines specific BGR color ranges for red and blue object detection
- Generates binary masks highlighting regions of interest

### 3. Blob Detection

- Employs cv2.SimpleBlobDetector to identify connected regions (blobs) within the filtered images
- Configurable parameters for blob detection (e.g., area, inertia)
- Stores detected blob information (keypoints and associated colors)

### 4. Visualization

- Displays the original RGB image from the sensor
- Visualizes the color-filtered images (masks) for red and blue
- Overlays detected blobs on the original image

## Detection Capabilities

### Image Acquisition

- Initializes the RGB-D camera in CoppeliaSim
- Activates the RGB sensor and starts image streaming
- Retrieves the latest image frame from the sensor buffer

### Blob Detection Process

- Applies color filtering to the input image based on predefined color ranges
- Detects blobs in the filtered image using the SimpleBlobDetector
- Associates detected blobs (keypoints) with their corresponding colors
- Optionally, visualizes the detected blobs on the original image

## Example Operations

### Image Acquisition and Display

```python
# Get an image from the sensor
image = image_controller.get_image()
# Display the image
if image is not None:
    cv2.imshow("Original Image", image)
```

### Color Filtering and Blob Detection

```python
# Filter for red blobs
red_mask, red_keypoints = image_controller.get_filtered_image(image, Color.RED)
# Filter for blue blobs
blue_mask, blue_keypoints = image_controller.get_filtered_image(image, Color.BLUE)

# Display the filtered images
cv2.imshow("Red Filtered", red_mask)
cv2.imshow("Blue Filtered", blue_mask)
```

## Visualization Output

### Generated Images

- **Original Image**: The raw RGB image from the camera
- **Red Filtered**: A binary mask showing detected red regions
- **Blue Filtered**: A binary mask showing detected blue regions

## Usage

1. Start CoppeliaSim
2. Load scene: `scenes/colors.ttt`
3. Run: `python exercise8.py`

## Results

Successfully implemented:

- ✅ Image Capture: Acquiring RGB images from a simulated camera in CoppeliaSim
- ✅ Color Filtering: Isolating red and blue objects using color thresholds
- ✅ Blob Detection: Identifying colored objects as distinct blobs
- ✅ Visualization: Displaying original and processed images
