from __future__ import annotations

from pathlib import Path
from typing import Tuple, List, Dict, Set


def debug(dots: Set[Tuple[int, int]]):
    size = [0, 0]
    for x, y in dots:
        if x > size[0]:
            size[0] = x
        if y > size[1]:
            size[1] = y

    output = ''
    for y in range(0, size[1] + 1):
        for x in range(0, size[0] + 1):
            output += '#' if (x, y) in dots else '.'
        output += '\n'

    print(output)


def part1(input: str, num_folds: int = 0) -> int:
    dots: Set[Tuple[int, int]] = set()
    folds: List[str] = []
    read_folds = False
    size = [0, 0]

    for line in input.splitlines():
        if line == "":
            read_folds = True
            continue

        if read_folds:
            folds.append(line.removeprefix("fold along "))
        else:
            x, y = map(int, line.split(","))

            dots.add((x, y))

            if x > size[0]:
                size[0] = x
            if y > size[1]:
                size[1] = y

    debug(dots)

    for n, instruction in enumerate(folds):
        if 0 < num_folds == n:
            break

        axis, position = instruction.split('=')
        position = int(position)

        for dot in list(dots):
            if axis == 'y' and dot[1] < position:
                continue
            if axis == 'x' and dot[0] < position:
                continue

            dots.remove(dot)

            if axis == 'y':
                dots.add((dot[0], dot[1] - (dot[1] - position) * 2))
            else:
                dots.add((dot[0] - (dot[0] - position) * 2, dot[1]))

        debug(dots)
        print(instruction, len(dots))
        print()

    return len(dots)


def part2(input: str) -> int:
    return 0


if __name__ == '__main__':
    example = '\n'.join([
        "6,10",
        "0,14",
        "9,10",
        "0,3",
        "10,4",
        "4,11",
        "6,0",
        "6,12",
        "4,1",
        "0,13",
        "10,12",
        "3,4",
        "3,0",
        "8,4",
        "1,10",
        "2,14",
        "8,10",
        "9,0",
        "",
        "fold along y=7",
        "fold along x=5",
    ])

    input = Path('./input.txt').read_text()

    example_part1 = part1(example, 1)
    assert example_part1 == 17, f"got {example_part1}"
    print(part1(input, 1))
    print(part1(input))

    # example_part2 = part2(example)
    # assert example_part2 == 195, f"got {example_part2}"
    # print(part2(input))
