from typing import List, Sequence, TypeVar

T = TypeVar("T")


def to_matrix(vec: Sequence[T], n: int) -> list[Sequence[T]]:
    return [vec[i : i + n] for i in range(0, len(vec), n)]


def transform(vec: List[T]) -> list[Sequence[T]]:
    vec.pop(0)
    vec.pop(0)
    return to_matrix(vec, 4)
