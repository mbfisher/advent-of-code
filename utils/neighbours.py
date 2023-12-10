from enum import Enum
from typing import Tuple, Iterator

class Direction(Enum):
    N = (-1, 0)
    NE = (-1, 1)
    E = (0, 1)
    SE = (1, 1)
    S = (1, 0)
    SW = (1, -1)
    W = (0, -1)
    NW = (-1, -1)

DIRECTIONS_ALL = (
    Direction.N,
    Direction.NE,
    Direction.E,
    Direction.SE,
    Direction.S,
    Direction.SW,
    Direction.W,
    Direction.NW,
)

DIRECTIONS_CARDINAL = (
    Direction.N,
    Direction.E,
    Direction.S,
    Direction.W,
)

Grid = Tuple[Tuple[str, ...], ...]
Position = Tuple[int, int]


def neighbours(position: Position, grid: Grid, directions=DIRECTIONS_ALL) -> Iterator[Tuple[Position, Direction]]:
    r, c = position

    for direction in directions:
        dr, dc = r + direction.value[0], c + direction.value[1]

        if dr < 0 or dr > len(grid) - 1 or dc < 0 or dc > len(grid[0]) - 1:
            continue

        yield (dr, dc), direction
