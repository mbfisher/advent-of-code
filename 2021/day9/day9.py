from __future__ import annotations

from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional

import math


def part1(input: str) -> int:
    heightmap: List[List[int]] = [list(map(int, row)) for row in input.splitlines()]

    def get_value(row: int, col: int):
        try:
            return heightmap[row][col]
        except IndexError:
            return None

    result = 0

    for row_index, row in enumerate(heightmap):
        for col_index in range(0, len(row)):
            adjacent = filter(lambda v: v is not None, [
                # top
                get_value(row_index - 1, col_index),
                # right
                get_value(row_index, col_index + 1),
                # bottom
                get_value(row_index + 1, col_index),
                # left
                get_value(row_index, col_index - 1)
            ])

            value = heightmap[row_index][col_index]

            if all([value < a for a in adjacent]):
                result += value + 1

    return result


def part2(input: str) -> int:
    heightmap: List[List[int]] = [list(map(int, row)) for row in input.splitlines()]

    def get_basin(row: int, col: int, depth=0) -> Set[Tuple[int, int]]:
        basin: Set[Tuple[int, int]] = set()
        basin.add((row, col))

        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        queue = set()
        queue.add((row, col))

        while queue:
            for coord in list(queue):
                for direction in directions:
                    location = coord

                    while True:
                        location = (location[0] + direction[0], location[1] + direction[1])

                        if location in basin:
                            continue

                        next_row, next_col = location

                        if next_row < 0 or next_col < 0:
                            break

                        try:
                            value = heightmap[next_row][next_col]
                            if value != 9:
                                basin.add((next_row, next_col))
                                queue.add((next_row, next_col))
                            else:
                                raise IndexError
                        except IndexError:
                            break

                queue.remove(coord)

        return basin

    basins: List[Set[Tuple[int, int]]] = []
    visited = {}

    for row_index, row in enumerate(heightmap):
        for col_index in range(0, len(row)):
            if (row_index, col_index) in visited:
                continue

            value = heightmap[row_index][col_index]

            if value == 9:
                continue

            basin = get_basin(row_index, col_index)
            basins.append(basin)

            for coord in basin:
                visited[coord] = True

    sorted_basins = sorted(basins, key=len, reverse=True)

    return math.prod(map(len, sorted_basins[0:3]))


if __name__ == '__main__':
    example = '\n'.join([
        "2199943210",
        "3987894921",
        "9856789892",
        "8767896789",
        "9899965678",
    ])

    input = Path('./input.txt').read_text()

    example_part1 = part1(example)
    assert example_part1 == 15, f"got {example_part1}"
    print(part1(input))

    example_part2 = part2(example)
    assert example_part2 == 1134, f"got {example_part2}"
    print(part2(input))
