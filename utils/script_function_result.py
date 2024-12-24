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
