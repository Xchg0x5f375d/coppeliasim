import csv
from dataclasses import dataclass
from typing import List


@dataclass
class ScriptFunctionResult:
    return_code: int
    output_ints: List[int]
    output_floats: List[float]
    output_strings: List[str]
    output_bytes: bytearray

    @property
    def success(self) -> bool:
        return self.return_code == 0

    @staticmethod
    def empty() -> "ScriptFunctionResult":
        return ScriptFunctionResult(
            return_code=0,
            output_ints=[],
            output_floats=[],
            output_strings=[],
            output_bytes=bytearray(),
        )

    @staticmethod
    def from_csv(filepath: str) -> "ScriptFunctionResult":
        """
        FOR TEST PURPOSES ONLY. This method is intended for mocking and testing,
        specifically as a workaround for issues encountered when directly calling
        the `simxCallScriptFunction` API in V-REP. It is observed that
        `simxCallScriptFunction` might not consistently return the expected data
        structure or may exhibit unexpected behavior in certain V-REP versions or
        configurations.
        """
        try:
            with open(filepath, "r") as file:
                reader = csv.reader(file)
                next(reader, None)
                output_floats = [float(row[0]) for row in reader if row]
                return ScriptFunctionResult(
                    return_code=0,  # Assume success
                    output_ints=[],
                    output_floats=output_floats,
                    output_strings=[],
                    output_bytes=bytearray(),
                )
        except (FileNotFoundError, ValueError, csv.Error) as e:
            print(f"Error reading or parsing CSV: {e}")
        return ScriptFunctionResult.empty()
