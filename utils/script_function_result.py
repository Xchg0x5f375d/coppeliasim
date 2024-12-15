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
