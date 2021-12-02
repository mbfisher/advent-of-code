from pathlib import Path
from typing import List


def part1(input: str) -> int:
    position = 0
    depth = 0

    for instruction in input.split("\n"):
        direction, magnitude = instruction.split(" ")

        if direction == "forward":
            position += int(magnitude)
        if direction == "up":
            depth -= int(magnitude)
        if direction == "down":
            depth += int(magnitude)

    return position * depth


def part2(input: str) -> int:
    position = 0
    depth = 0
    aim = 0

    for instruction in input.split("\n"):
        direction, magnitude = instruction.split(" ")

        if direction == "forward":
            position += int(magnitude)
            depth += int(magnitude) * aim
        if direction == "up":
            aim -= int(magnitude)
        if direction == "down":
            aim += int(magnitude)

    return position * depth


if __name__ == '__main__':
    example = '\n'.join([
        "forward 5",
        "down 5",
        "forward 8",
        "up 3",
        "down 8",
        "forward 2"
    ])

    assert part1(example) == 150
    print(part1(Path('./input.txt').read_text()))

    assert part2(example) == 900
    print(part2(Path('./input.txt').read_text()))
