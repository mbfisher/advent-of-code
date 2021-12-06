import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, TypedDict, Dict, Set, Tuple, Optional


@dataclass
class Point:
    x: int
    y: int

    def __init__(self, x: int = None, y: int = None, coords: str = None) -> None:
        super().__init__()
        if coords:
            x, y = tuple(map(int, coords.split(",", 2)))

        self.x = x
        self.y = y

    def __add__(self, other: Tuple[int, int]):
        return Point(x=self.x + other[0], y=self.y + other[1])

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"{self.x},{self.y}"

    def __repr__(self):
        return str(self)


@dataclass
class Line:
    start: Point
    end: Point


def part1(input: str) -> int:
    lines: List[Line] = []

    for input_line in input.splitlines():
        start, end = input_line.split(" -> ")
        lines.append(Line(start=Point(coords=start), end=Point(coords=end)))

    horizontal_lines: List[Line] = list(
        filter(lambda line: line.start.x == line.end.x or line.start.y == line.end.y, lines))
    points: Dict[str, int] = {}

    for line in horizontal_lines:
        delta: Tuple[int, int]
        if line.start.x < line.end.x:
            delta = (1, 0)
        elif line.start.x > line.end.x:
            delta = (-1, 0)
        elif line.start.y < line.end.y:
            delta = (0, 1)
        else:
            delta = (0, -1)

        if str(line.start) not in points:
            points[str(line.start)] = 0
        points[str(line.start)] += 1

        point = line.start
        while point != line.end:
            point = point + delta

            if str(point) not in points:
                points[str(point)] = 0
            points[str(point)] += 1

    return len([point for point, count in points.items() if count >= 2])


def part2(input: str) -> int:
    lines: List[Line] = []

    for input_line in input.splitlines():
        start, end = input_line.split(" -> ")
        lines.append(Line(start=Point(coords=start), end=Point(coords=end)))

    points: Dict[str, int] = {}

    for line in lines:
        delta: Tuple[int, int]

        dy = line.start.y - line.end.y
        dx = line.start.x - line.end.x
        gradient = float(dy) / float(dx) if dx != 0 else 0

        if dx == 0:
            delta = (0, 1 if line.end.y > line.start.y else -1)
        elif gradient == 0:
            delta = (1 if line.end.x > line.start.x else -1, 0)
        else:
            delta = (1 if line.end.x > line.start.x else -1, 1 if line.end.y > line.start.y else -1)

        print(line, dx, dy, gradient, delta)

        if str(line.start) not in points:
            points[str(line.start)] = 0
        points[str(line.start)] += 1

        point = line.start
        while point != line.end:
            point = point + delta

            if str(point) not in points:
                points[str(point)] = 0
            points[str(point)] += 1

    return len([point for point, count in points.items() if count >= 2])


if __name__ == '__main__':
    example = '\n'.join([
        "0,9 -> 5,9",
        "8,0 -> 0,8",
        "9,4 -> 3,4",
        "2,2 -> 2,1",
        "7,0 -> 7,4",
        "6,4 -> 2,0",
        "0,9 -> 2,9",
        "3,4 -> 1,4",
        "0,0 -> 8,8",
        "5,5 -> 8,2",
    ])

    input = Path('./input.txt').read_text()

    example_part1 = part1(example)
    assert example_part1 == 5, f"got {example_part1}"
    print(part1(input))

    example_part2 = part2(example)
    assert example_part2 == 12, f"got {example_part2}"
    print(part2(input))
