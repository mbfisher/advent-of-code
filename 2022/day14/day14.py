import json
import unittest
from collections import deque
from pathlib import Path


def part1(input: str) -> int:
    rock_tiles = set()
    x = 0
    y = 1

    max_x = 0
    max_y = 0

    for line in input.split("\n"):
        path = []
        points = line.split(" -> ")
        for point in points:
            path.append(tuple(map(int, point.split(","))))

        for i in range(0, len(path) - 1):
            start, end = path[i], path[i + 1]
            increment = (0, -1 if end[y] - start[y] < 0 else 1) if start[x] == end[x] \
                else (-1 if end[x] - start[x] < 0 else 1, 0)

            point = start
            done = False
            while True:
                rock_tiles.add(point)

                if point[x] > max_x:
                    max_x = point[x]
                if point[y] > max_y:
                    max_y = point[y]

                if done:
                    break

                point = (point[x] + increment[x], point[y] + increment[y])

                if point[x] == end[x] and point[y] == end[y]:
                    done = True

    # for i in range(0, 10):
    #     print(''.join(['#' if (j, i) in rock_tiles else '.' for j in range(494, 504)]))

    sand_unit = (500, 0)
    sand_at_rest = set()

    down = (0, 1)
    down_left = (-1, 1)
    down_right = (1, 1)
    while True:
        blocked = True
        for move in [down, down_left, down_right]:
            next_sand = sand_unit[x] + move[x], sand_unit[y] + move[y]
            if next_sand not in rock_tiles and next_sand not in sand_at_rest:
                sand_unit = next_sand
                blocked = False
                break

        if blocked:
            sand_at_rest.add(sand_unit)
            # print()
            # for i in range(0, 10):
            #     print(''.join(['o' if (j, i) in sand_at_rest else '#' if (j, i) in rock_tiles else '.' for j in range(494, 504)]))
            sand_unit = (500, 0)
        else:
            if not 0 <= sand_unit[x] <= max_x or not 0 <= sand_unit[y] <= max_y:
                break

    return len(sand_at_rest)


def part2(input: str) -> int:
    rock_tiles = set()
    x = 0
    y = 1

    max_x = 0
    max_y = 0

    for line in input.split("\n"):
        path = []
        points = line.split(" -> ")
        for point in points:
            path.append(tuple(map(int, point.split(","))))

        for i in range(0, len(path) - 1):
            start, end = path[i], path[i + 1]
            increment = (0, -1 if end[y] - start[y] < 0 else 1) if start[x] == end[x] \
                else (-1 if end[x] - start[x] < 0 else 1, 0)

            point = start
            done = False
            while True:
                rock_tiles.add(point)

                if point[x] > max_x:
                    max_x = point[x]
                if point[y] > max_y:
                    max_y = point[y]

                if done:
                    break

                point = (point[x] + increment[x], point[y] + increment[y])

                if point[x] == end[x] and point[y] == end[y]:
                    done = True

    floor_y = max_y + 2

    # for i in range(0, 12):
    #     print(''.join(['#' if (j, i) in rock_tiles or i == floor_y else '.' for j in range(500-12, 500+13)]))

    sand_unit = (500, 0)
    sand_at_rest = set()

    down = (0, 1)
    down_left = (-1, 1)
    down_right = (1, 1)
    while True:
        blocked = True
        for move in [down, down_left, down_right]:
            next_sand = sand_unit[x] + move[x], sand_unit[y] + move[y]
            if next_sand not in rock_tiles and next_sand not in sand_at_rest and next_sand[y] < floor_y:
                sand_unit = next_sand
                blocked = False
                break

        if blocked:
            sand_at_rest.add(sand_unit)

            # print()
            # for i in range(0, 12):
            #     print(''.join(['o' if (j, i) in sand_at_rest else '#' if (j, i) in rock_tiles or i == floor_y else '.' for j in range(500-12, 500+13)]))

            if sand_unit == (500, 0):
                break

            sand_unit = (500, 0)

    return len(sand_at_rest)


class Test(unittest.TestCase):

    def test_part_1(self):
        self.assertEqual(24, part1(Test.example))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(93, part2(Test.example))

        print(part2(Path('./input.txt').read_text()))

    example = """
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9""".strip("\n")
