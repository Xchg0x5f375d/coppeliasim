from typing import List, Optional, Tuple

import numpy as np

from utils import vrep


class VREPConnection:
    def __init__(self, address: str = "127.0.0.1", port: int = 19997) -> None:
        self.__address = address
        self.__port = port
        self.__client_id: Optional[int] = None
        self.connect()
        self.start_simulation()

    def connect(self) -> bool:
        print("Program started")
        vrep.simxFinish(-1)
        self.__client_id = vrep.simxStart(
            connectionAddress=self.__address,
            connectionPort=self.__port,
            waitUntilConnected=True,
            doNotReconnectOnceDisconnected=True,
            timeOutInMs=2000,
            commThreadCycleInMs=5,
        )
        if self.__client_id == -1:
            print("Failed connecting to remote API server")
            return False
        print("Connected to remote API server")
        return True

    def disconnect(self) -> bool:
        if self.__client_id is None:
            return False
        self.stop_simulation()
        vrep.simxFinish(self.__client_id)
        print("Program ended")
        return True

    def start_simulation(self) -> bool:
        if self.__client_id is None:
            return False
        status = vrep.simxStartSimulation(self.__client_id, vrep.simx_opmode_blocking)
        if status != vrep.simx_return_ok:
            print(f"Failed to start simulation: error code {status}")
            return False
        return True

    def stop_simulation(self) -> bool:
        if self.__client_id is None:
            return False
        status = vrep.simxStopSimulation(self.__client_id, vrep.simx_opmode_blocking)
        if status != vrep.simx_return_ok:
            print(f"Failed to stop simulation: error code {status}")
            return False
        return True

    def get_object_handle(
        self, name: str, operation_mode: int = vrep.simx_opmode_blocking
    ) -> Optional[Tuple[int, int]]:
        if self.__client_id is None:
            return None
        status, handle = vrep.simxGetObjectHandle(
            self.__client_id, name, operation_mode
        )
        if status != vrep.simx_return_ok:
            print(f"Failed to get handle for {name}: error code {status}")
            return None
        return status, handle

    def get_object_position(
        self,
        object_handle: int,
        reference_handle: int = -1,
        operation_mode: int = vrep.simx_opmode_blocking,
    ) -> Tuple[int, np.ndarray]:
        if self.__client_id is None:
            return -1, np.zeros(3)
        return vrep.simxGetObjectPosition(
            self.__client_id, object_handle, reference_handle, operation_mode
        )

    def get_object_orientation(
        self,
        object_handle: int,
        reference_handle: int = -1,
        operation_mode: int = vrep.simx_opmode_blocking,
    ) -> Tuple[int, np.ndarray]:
        if self.__client_id is None:
            return -1, np.zeros(3)
        return vrep.simxGetObjectOrientation(
            self.__client_id, object_handle, reference_handle, operation_mode
        )

    def get_ping_time(self) -> int:
        if self.__client_id is None:
            return -1
        return vrep.simxGetPingTime(self.__client_id)

    def set_object_position(
        self,
        name: str,
        position: Tuple[float, float, float],
        operation_mode: int = vrep.simx_opmode_blocking,
    ) -> None:
        print(f"Attempting to set position for object: {name}")
        _, handle = self.get_object_handle(name, operation_mode)
        vrep.simxSetObjectPosition(
            self.__client_id, handle, -1, position, operation_mode
        )

    def set_joint_target_velocity(
        self, joint_handle, velocity, operation_mode=vrep.simx_opmode_oneshot
    ) -> None:
        if self.__client_id is None:
            return
        vrep.simxSetJointTargetVelocity(
            self.__client_id, joint_handle, velocity, operation_mode
        )

    def set_joint_target_position(
        self, joint_handle, angle, operation_mode=vrep.simx_opmode_oneshot
    ) -> None:
        if self.__client_id is None:
            return
        vrep.simxSetJointTargetPosition(
            self.__client_id, joint_handle, angle, operation_mode
        )

    def set_integer_signal(
        self, signal: Tuple[str, int], operation_mode=vrep.simx_opmode_oneshot
    ) -> int:
        if self.__client_id is None:
            return -1
        signal_name, signal_value = signal
        return vrep.simxSetIntegerSignal(
            self.__client_id, signal_name, signal_value, operation_mode
        )

    def read_vision_sensor(
        self,
        sensor_handle: Optional[Tuple[int, int]],
        operation_mode=vrep.simx_opmode_streaming,
    ) -> Tuple[int, bool, List[List[float]]]:
        if self.__client_id is None:
            return -1, False, []
        return_code, detection_state, aux_values = vrep.simxReadVisionSensor(
            self.__client_id, sensor_handle, operation_mode
        )
        return return_code, detection_state, aux_values

    def __del__(self):
        self.disconnect()
