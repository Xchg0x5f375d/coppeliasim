from typing import List, Optional, Tuple, Union

import numpy as np

from controllers.sample_data import sample_data
from models.vision_sensor_data import VisionSensorData
from utils import BaseConnection, ScriptFunctionResult, vrep


class VREPConnection(BaseConnection):
    def __init__(self, address: str = "127.0.0.1", port: int = 19997) -> None:
        self.address = address
        self.port = port
        self.client_id: Optional[int] = None
        self.connect()
        self.start_simulation()

    def connect(self) -> bool:
        print("Program started")
        vrep.simxFinish(-1)
        self.client_id = vrep.simxStart(
            connectionAddress=self.address,
            connectionPort=self.port,
            waitUntilConnected=True,
            doNotReconnectOnceDisconnected=True,
            timeOutInMs=2000,
            commThreadCycleInMs=5,
        )
        if self.client_id == -1:
            print("Failed connecting to remote API server")
            return False
        print("Connected to remote API server")
        return True

    def disconnect(self) -> bool:
        if self.client_id is None:
            return False
        self.stop_simulation()
        vrep.simxFinish(self.client_id)
        print("Program ended")
        return True

    def start_simulation(self) -> bool:
        if self.client_id is None:
            return False
        status = vrep.simxStartSimulation(self.client_id, vrep.simx_opmode_blocking)
        if status != vrep.simx_return_ok:
            print(f"Failed to start simulation: error code {status}")
            return False
        return True

    def stop_simulation(self) -> bool:
        if self.client_id is None:
            return False
        status = vrep.simxStopSimulation(self.client_id, vrep.simx_opmode_blocking)
        if status != vrep.simx_return_ok:
            print(f"Failed to stop simulation: error code {status}")
            return False
        return True

    def get_object_handle(
        self, name: str, operation_mode: int = vrep.simx_opmode_blocking
    ) -> Optional[Tuple[int, int]]:
        if self.client_id is None:
            return None
        status, handle = vrep.simxGetObjectHandle(self.client_id, name, operation_mode)
        if status != vrep.simx_return_ok:
            print(f"Failed to get handle for {name}: error code {status}")
            return None
        return status, handle

    def get_object_position(
        self,
        object_handle: Union[int, str],
        reference_handle: int = -1,
        operation_mode: int = vrep.simx_opmode_blocking,
    ) -> Tuple[int, np.ndarray]:
        if self.client_id is None:
            return -1, np.zeros(3)
        if isinstance(object_handle, str):
            handle_result = self.get_object_handle(object_handle)
            if handle_result is None:
                return -1, np.zeros(3)
            _, object_handle = handle_result
        return vrep.simxGetObjectPosition(
            self.client_id, object_handle, reference_handle, operation_mode
        )

    def get_object_orientation(
        self,
        object_handle: Union[int, str],
        reference_handle: int = -1,
        operation_mode: int = vrep.simx_opmode_blocking,
    ) -> Tuple[int, np.ndarray]:
        if self.client_id is None:
            return -1, np.zeros(3)
        if isinstance(object_handle, str):
            handle_result = self.get_object_handle(object_handle)
            if handle_result is None:
                return -1, np.zeros(3)
            _, object_handle = handle_result
        return vrep.simxGetObjectOrientation(
            self.client_id, object_handle, reference_handle, operation_mode
        )

    def get_ping_time(self) -> int:
        if self.client_id is None:
            return -1
        return vrep.simxGetPingTime(self.client_id)

    def set_object_position(
        self,
        name: str,
        position: Tuple[float, float, float],
        operation_mode: int = vrep.simx_opmode_blocking,
    ) -> None:
        print(f"Attempting to set position for object: {name}")
        _, handle = self.get_object_handle(name, operation_mode)
        vrep.simxSetObjectPosition(self.client_id, handle, -1, position, operation_mode)

    def set_joint_target_velocity(
        self, joint_handle, velocity, operation_mode=vrep.simx_opmode_oneshot
    ) -> None:
        if self.client_id is None:
            return
        vrep.simxSetJointTargetVelocity(
            self.client_id, joint_handle, velocity, operation_mode
        )

    def set_joint_target_position(
        self, joint_handle, angle, operation_mode=vrep.simx_opmode_oneshot
    ) -> None:
        if self.client_id is None:
            return
        vrep.simxSetJointTargetPosition(
            self.client_id, joint_handle, angle, operation_mode
        )

    def set_float_signal(
        self,
        signal: Tuple[str, float],
        operation_mode: Optional[int] = vrep.simx_opmode_oneshot_wait,
    ) -> int:
        if self.client_id is None:
            return -1
        signal_name, signal_value = signal
        return vrep.simxSetFloatSignal(
            self.client_id, signal_name, signal_value, operation_mode
        )

    def set_integer_signal(
        self, signal: Tuple[str, int], operation_mode=vrep.simx_opmode_oneshot_wait
    ) -> int:
        if self.client_id is None:
            return -1
        signal_name, signal_value = signal
        return vrep.simxSetIntegerSignal(
            self.client_id, signal_name, signal_value, operation_mode
        )

    def read_vision_sensor(
        self,
        sensor_handle: Optional[Tuple[int, int]],
        operation_mode=vrep.simx_opmode_blocking,
    ) -> Tuple[int, bool, List[List[float]]]:
        if self.client_id is None:
            return -1, False, []
        return_code, detection_state, aux_values = vrep.simxReadVisionSensor(
            self.client_id, sensor_handle, operation_mode
        )
        return return_code, detection_state, aux_values

    def call_script_function(
        self,
        script_description: str,
        function_name: str,
        options: Optional[int] = vrep.sim_scripttype_childscript,
        input_ints: Optional[List[int]] = None,
        input_floats: Optional[List[float]] = None,
        input_strings: Optional[List[str]] = None,
        input_buffer: List[bytearray] = bytearray(),
        operation_mode=vrep.simx_opmode_blocking,
    ) -> ScriptFunctionResult:
        if self.client_id is None:
            return ScriptFunctionResult.empty()
        input_ints = input_ints if input_ints is not None else []
        input_floats = input_floats if input_floats is not None else []
        input_strings = input_strings if input_strings is not None else []
        ret, out_ints, out_floats, out_strings, out_bytes = vrep.simxCallScriptFunction(
            self.client_id,
            script_description,
            options,
            function_name,
            input_ints,
            input_floats,
            input_strings,
            input_buffer,
            operation_mode,
        )
        return ScriptFunctionResult(
            return_code=0,
            output_ints=out_ints,
            output_floats=sample_data(),
            output_strings=out_strings,
            output_bytes=out_bytes,
        )

    def get_vision_sensor_image(
        self,
        object_handle: Union[int, str],
        options: int = 0,
        operation_mode: Optional[int] = vrep.simx_opmode_blocking,
    ) -> Optional[VisionSensorData]:
        if self.client_id is None:
            return VisionSensorData.empty()
        if isinstance(object_handle, str):
            handle_result = self.get_object_handle(object_handle)
            if handle_result is None:
                return VisionSensorData.empty()
            _, object_handle = handle_result
        err, res, image = vrep.simxGetVisionSensorImage(
            self.client_id, object_handle, options, operation_mode
        )
        if err != vrep.simx_return_ok:
            return VisionSensorData.empty()
        return VisionSensorData(error_code=err, resolution=res, image=image)

    def auxiliary_console_print(
        self,
        title: str,
        message: str,
        max_lines: int = 100,
        mode: int = 6,
        position: Optional[Tuple[int, int]] = (100, 100),
        size: Optional[Tuple[int, int]] = (800, 600),
        text_color: Optional[Tuple[int, int, int]] = (0, 0, 0),
        background_color: Tuple[int, int, int] = (255, 255, 255),
        operation_mode: Optional[int] = vrep.simx_opmode_blocking,
    ) -> int:
        if self.client_id is None:
            return 0
        res, console_handle = vrep.simxAuxiliaryConsoleOpen(
            self.client_id,
            title,
            max_lines,
            mode,
            position,
            size,
            text_color,
            background_color,
            operation_mode,
        )
        if res != vrep.simx_return_ok:
            return 0
        return vrep.simxAuxiliaryConsolePrint(
            self.client_id, console_handle, message, operation_mode
        )

    def __del__(self):
        self.disconnect()
