import cv2

from controllers.image_controller import Color
from robot.robot import Robot


def main():
    robot = Robot()
    original_image = robot.image_controller.get_image()
    while True:
        if original_image is not None:
            red_filtered, red_keypoints = robot.image_controller.get_filtered_image(
                original_image, Color.RED
            )
            blue_filtered, blue_keypoints = (
                robot.image_controller.get_filtered_image(
                    original_image, Color.BLUE
                )
            )
            cv2.imshow("Original Image", original_image)
            cv2.imshow("Red Filtered", red_filtered)
            cv2.imshow("Blue Filtered", blue_filtered)
            if cv2.waitKey(1) == ord("q"):
                break


if __name__ == "__main__":
    main()
