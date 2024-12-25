from typing import List, Sequence, TypeVar

import numpy as np

T = TypeVar("T")


class LinAlgUtils:
    # =====================================================================
    # Matrices Functions
    # =====================================================================

    @staticmethod
    def to_matrix(vec: Sequence[T], n: int) -> List[Sequence[T]]:
        return [vec[i : i + n] for i in range(0, len(vec), n)]

    @staticmethod
    def transform(vec: List[T]) -> List[Sequence[T]]:
        vec.pop(0)
        vec.pop(0)
        return LinAlgUtils.to_matrix(vec, 4)

    # =====================================================================
    # Vectors Functions
    # =====================================================================

    @staticmethod
    def de_eulerize(euler: Sequence[float]) -> np.ndarray:
        x = euler[1] / (np.pi / 2) * -1.0
        y = 0.0
        if euler[0] > 0:
            y = 1.0 - abs(euler[1] / (np.pi / 2))
        else:
            y = abs(euler[1] / (np.pi / 2)) - 1.0
        return LinAlgUtils.normalize_vector([x, y])

    @staticmethod
    def normalize_vector(v: List[float]) -> np.ndarray:
        norm = np.linalg.norm(v)
        if norm == 0:
            return np.array(v)
        return np.array(v) / norm

    # =====================================================================
    # Degree-related Functions
    # =====================================================================

    @staticmethod
    def normalize_degrees(deg: float) -> float:
        return deg % 360

    # =====================================================================
    # Miscellaneous Functions
    # =====================================================================

    @staticmethod
    def vector_length(vec: List[float]) -> float:
        return np.sqrt(vec[0] ** 2 + vec[1] ** 2)
