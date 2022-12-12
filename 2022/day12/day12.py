import unittest
from collections import deque
from math import prod
from pathlib import Path
from queue import PriorityQueue


def part1(input: str) -> int:
    grid = []
    start = None
    end = None

    visited = set()
    distances = {}

    for y, line in enumerate(input.split("\n")):
        row = []
        for x, elevation in enumerate(line):
            distances[(y, x)] = float('inf')

            if elevation == "S":
                start = (y, x)
                row.append(ord('a'))
            elif elevation == "E":
                end = (y, x)
                row.append(ord('z'))
            else:
                row.append(ord(elevation))
        grid.append(row)

    distances[start] = 0
    queue = PriorityQueue()
    queue.put((0, [start]))

    while not queue.empty():
        # print(queue.qsize())
        distance, path = queue.get()
        position = path[-1]
        elevation = grid[position[0]][position[1]]
        elevation_label = chr(elevation)

        # print()
        # for y, row in enumerate(grid):
        #     line = ['*' if (y, x) == position else '#' if (y, x) in path else '.' for x in range(len(row))]
        #     print(''.join(line))

        if position == end:
            break

        visited.add(position)

        destinations = []
        for dy, dx in [
            (-1, 0),  # up
            (0, 1),  # right
            (1, 0),  # down
            (0, -1)  # left
        ]:
            destination = (position[0] + dy, position[1] + dx)

            if 0 <= destination[0] < len(grid) and 0 <= destination[1] < len(grid[0]):
                next_elevation = grid[destination[0]][destination[1]]
                next_elevation_label = chr(next_elevation)
                if next_elevation <= elevation + 1:
                    destinations.append(destination)

        for destination in filter(lambda d: d not in visited, destinations):
            distance = distances[position] + 1
            if distance < distances[destination]:
                next_path = path + [destination]
                queue.put((distance, next_path))
                distances[destination] = distance

    return distances[end]


def part2(input: str) -> str:
    grid = []
    starts = set()
    end = None

    visited = set()
    distances = {}

    for y, line in enumerate(input.split("\n")):
        row = []
        for x, elevation in enumerate(line):
            distances[(y, x)] = float('inf')

            if elevation == "S" or elevation == "a":
                starts.add((y, x))
                row.append(ord('a'))
            elif elevation == "E":
                end = (y, x)
                row.append(ord('z'))
            else:
                row.append(ord(elevation))
        grid.append(row)

    queue = PriorityQueue()
    for start in starts:
        distances[start] = 0
        queue.put((0, [start]))

    while not queue.empty():
        # print(queue.qsize())
        distance, path = queue.get()
        position = path[-1]
        elevation = grid[position[0]][position[1]]
        elevation_label = chr(elevation)

        # print()
        # for y, row in enumerate(grid):
        #     line = ['*' if (y, x) == position else '#' if (y, x) in path else '.' for x in range(len(row))]
        #     print(''.join(line))

        if position == end:
            break

        visited.add(position)

        destinations = []
        for dy, dx in [
            (-1, 0),  # up
            (0, 1),  # right
            (1, 0),  # down
            (0, -1)  # left
        ]:
            destination = (position[0] + dy, position[1] + dx)

            if 0 <= destination[0] < len(grid) and 0 <= destination[1] < len(grid[0]):
                next_elevation = grid[destination[0]][destination[1]]
                next_elevation_label = chr(next_elevation)
                if next_elevation <= elevation + 1:
                    destinations.append(destination)

        for destination in filter(lambda d: d not in visited, destinations):
            distance = distances[position] + 1
            if distance < distances[destination]:
                next_path = path + [destination]
                queue.put((distance, next_path))
                distances[destination] = distance

    return distances[end]


class Test(unittest.TestCase):

    def test_part_1(self):
        self.assertEqual(31, part1(Test.example))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(29, part2(Test.example))

        print(part2(Path('./input.txt').read_text()))

    example = """
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi""".strip("\n")
