import re
import unittest
from math import prod
from pathlib import Path
from typing import Tuple


def move(robot, h, v) -> Tuple[int, int, int, int]:
    x, y, vx, vy = robot
    return (x + vx) % h, (y + vy) % v, vx, vy


def safety_factor(input: str, time: int = 100, h: int = 101, v: int = 103) -> int:
    pattern = re.compile(r'-*\d+')

    robots = [tuple(map(int, pattern.findall(line))) for line in input.splitlines()]

    for _ in range(time):
        for i, robot in enumerate(robots):
            robots[i] = move(robot, h, v)

    quadrants = {
        (0, 0): 0,
        (0, 1): 0,
        (1, 0): 0,
        (1, 1): 0
    }

    space = [[' ' if x == h // 2 or y == v // 2 else 0 for x in range(h)] for y in range(v)]

    for x, y, _, _ in robots:
        if x == h // 2 or y == v // 2:
            continue

        space[y][x] += 1
        q = (int(x > h // 2), int(y > v // 2))
        quadrants[q] += 1

    print("\n".join("".join("." if tile == 0 else str(tile) for tile in row) for row in space))

    return prod(quadrants.values())


def part1(input: str) -> int:
    return safety_factor(input)


def christmas_tree(input: str, h=101, v=103) -> int:
    pattern = re.compile(r'-*\d+')

    robots = []
    space = [[0 for _ in range(h)] for _ in range(v)]
    for line in input.splitlines():
        x, y, vx, vy = tuple(map(int, pattern.findall(line)))
        space[y][x] += 1
        robots.append((x, y, vx, vy))

    t = 0
    while True:
        t += 1
        rows = {y: set() for y in range(v)}

        for i, robot in enumerate(robots):
            x, y, _, _ = robot
            space[y][x] -= 1

            robots[i] = move(robot, h, v)

            x, y, _, _ = robots[i]
            space[y][x] += 1

            rows[y].add(x)

        maybe_rows = 0

        for y, cols in rows.items():
            if maybe_rows == 5:
                print("\n".join("".join("." if tile == 0 else str(tile) for tile in row) for row in space), "\n")
                return t

            cols = tuple(1 if x in cols else 0 for x in range(h))

            i = 0
            j = 1

            while i < len(cols) and j < len(cols):
                if cols[i] > 0 and cols[j] > 0:
                    if j - i >= 5:
                        maybe_rows += 1
                        print(t, y, i, j)
                        break

                    j += 1

                else:
                    i = i + 1
                    j = i + 1


def part2(input: str) -> int:
    return christmas_tree(input)


class Test(unittest.TestCase):
    example1 = """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
    """.strip()

    example2 = """

    """.strip()

    def test_part_1(self):
        self.assertEqual((4, 1, 2, -3), move((2, 4, 2, -3), 11, 7))
        self.assertEqual((6, 5, 2, -3), move((4, 1, 2, -3), 11, 7))
        self.assertEqual((8, 2, 2, -3), move((6, 5, 2, -3), 11, 7))
        self.assertEqual((10, 6, 2, -3), move((8, 2, 2, -3), 11, 7))
        self.assertEqual((1, 3, 2, -3), move((10, 6, 2, -3), 11, 7))
        self.assertEqual(12, safety_factor(self.example1, h=11, v=7))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        print(part2(Path('./input.txt').read_text()))
