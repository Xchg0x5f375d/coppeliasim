import array
import time
from enum import Enum
from typing import Dict, Optional, Sequence, Tuple

import cv2
import numpy as np
from PIL import Image

from models import VisionSensorData
from utils import VREPConnection, vrep


class Color(Enum):
    RED = "r"
    BLUE = "b"


class ImageController:
    def __init__(self, vrep_connection: VREPConnection):
        self.vrep_connection: VREPConnection = vrep_connection
        self.image_generator: Optional[VisionSensorData] = None
        self.camera_handle: Optional[int] = None
        self.rgb_sensor_handle: Optional[int] = None
        self.depth_sensor_handle: Optional[int] = None
        self.keypoint_color: Dict[Tuple[float, float], Color] = {}
        blob_detector_params = cv2.SimpleBlobDetector.Params()
        blob_detector_params.minDistBetweenBlobs = 1
        blob_detector_params.filterByColor = True
        blob_detector_params.blobColor = 255
        blob_detector_params.filterByArea = True
        blob_detector_params.minArea = 100
        blob_detector_params.maxArea = 50000
        blob_detector_params.filterByCircularity = False
        blob_detector_params.filterByConvexity = False
        blob_detector_params.filterByInertia = True
        blob_detector_params.minInertiaRatio = 0.01
        blob_detector_params.maxInertiaRatio = 1
        self.detector = cv2.SimpleBlobDetector.create(blob_detector_params)
        self.detector2 = cv2.SimpleBlobDetector.create(blob_detector_params)
        self.__initialize_camera()

    def __initialize_camera(self) -> None:
        err_cam, self.camera_handle = self.vrep_connection.get_object_handle(
            "rgbdSensor"
        )
        err_rgb, self.rgb_sensor_handle = self.vrep_connection.get_object_handle(
            "rgbSensor"
        )
        err_depth, self.depth_sensor_handle = self.vrep_connection.get_object_handle(
            "xyzSensor"
        )
        if (
            err_cam != vrep.simx_return_ok
            or err_rgb != vrep.simx_return_ok
            or err_depth != vrep.simx_return_ok
        ):
            print(
                f"Error: Could not get handles for vision sensors. Return codes: {err_cam}, {err_rgb}, {err_depth}"
            )
            return
        self.vrep_connection.set_float_signal(("Scanner_scanAngle", np.radians(90)))
        self.vrep_connection.set_integer_signal(("handle_rgb_sensor", 1))
        self.vrep_connection.get_vision_sensor_image(
            self.camera_handle, operation_mode=vrep.simx_opmode_streaming
        )
        self.vrep_connection.get_vision_sensor_image(
            self.rgb_sensor_handle, operation_mode=vrep.simx_opmode_streaming
        )
        self.image_generator = self.vrep_connection.get_vision_sensor_image(
            self.rgb_sensor_handle, operation_mode=vrep.simx_opmode_streaming
        )
        time.sleep(0.5)

    def get_image(self) -> Optional[np.ndarray]:
        sensor_image = self.vrep_connection.get_vision_sensor_image(
            self.rgb_sensor_handle
        )
        if sensor_image.success:
            image_buffer = Image.frombytes(
                "RGB",
                (sensor_image.resolution[0], sensor_image.resolution[1]),
                bytes(array.array("b", sensor_image.image)),
                "raw",
                "RGB",
                0,
                1,
            )
            img = np.asarray(image_buffer)
            img = cv2.cvtColor(cv2.flip(img, 0), cv2.COLOR_RGB2BGR)
            return img
        elif sensor_image.error_code == vrep.simx_return_novalue_flag:
            print("No image yet")
        else:
            print(f"Error getting image: {sensor_image.error_code}")
        return None

    def get_filtered_image(
        self, image: np.ndarray, color: Color
    ) -> Tuple[np.ndarray, Sequence[cv2.KeyPoint]]:
        if color == Color.RED:
            lower_bound = np.array([0, 0, 80])
            upper_bound = np.array([50, 50, 255])
            detector = self.detector
        elif color == Color.BLUE:
            lower_bound = np.array([100, 0, 0])
            upper_bound = np.array([255, 50, 50])
            detector = self.detector2
        else:
            raise ValueError("Invalid color specified")
        mask = cv2.inRange(image, lower_bound, upper_bound)
        keypoints = detector.detect(mask)
        self.keypoint_color.clear()
        for kp in keypoints:
            self.keypoint_color[(kp.pt[0], kp.pt[1])] = color
        return mask, keypoints

    def __del__(self) -> None:
        cv2.destroyAllWindows()
