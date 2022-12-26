import unittest
from collections import deque
from pathlib import Path
from typing import Tuple, Dict

right, down, left, up = range(4)


def part1(input: str) -> int:
    y, x = 0, 1
    rows = {}
    columns = {}
    start = None
    path = []

    parse_path = False
    row = 1
    for line in input.split("\n"):
        if line == "":
            parse_path = True
            continue

        if parse_path:
            prev = None
            current = ""
            for char in line:
                if char.isnumeric() and prev is not None and not prev.isnumeric():
                    path.append(current)
                    current = char
                elif char.isalpha() and prev is not None and not prev.isalpha():
                    path.append(int(current))
                    current = char
                else:
                    current += char
                prev = char
        else:
            for i, char in enumerate(line):
                column = i + 1

                if start is None and char == ".":
                    start = [row, column]

                if char != ' ':
                    rows.setdefault(row, {}).setdefault(column, char)
                    columns.setdefault(column, {}).setdefault(row, char)

            row += 1

    path.append(int(current))

    bounds = (max(rows.keys()), max(columns.keys()))

    facings = (
        (0, 1),  # R
        (1, 0),  # D
        (0, -1),  # L
        (-1, 0),  # U
    )
    facing = 0

    position = start
    trace = {start[y]: {start[x]: facing}}

    def log():
        output = ""
        for row in range(1, bounds[y] + 1):
            line = ""
            for column in range(1, bounds[x] + 1):
                if [row, column] == position:
                    line += ["↦", "↧", "↤", "↥"][facing]
                elif row in trace and column in trace[row]:
                    line += [">", "v", "<", "^"][trace[row][column]]
                elif row in rows and column in rows[row]:
                    line += rows[row][column]
                else:
                    line += " "

            output += line + "\n"

        print(output)

    # print(position)
    # log()

    for instruction in path:
        # print(f"\n=== {instruction} ===\n")

        if type(instruction) == int:
            for _ in range(instruction):
                next_position = [position[y] + facings[facing][y], position[x] + facings[facing][x]]

                if rows.get(next_position[y], {}).get(next_position[x], None) is None:
                    if facing == 0:  # R
                        next_position[x] = min(rows[next_position[y]].keys())
                    elif facing == 1:  # D
                        next_position[y] = min(columns[next_position[x]].keys())
                    elif facing == 2:  # L
                        next_position[x] = max(rows[next_position[y]].keys())
                    elif facing == 3:  # U
                        next_position[y] = max(columns[next_position[x]].keys())

                if rows[next_position[y]][next_position[x]] == '.':
                    position = next_position
                    trace.setdefault(position[y], {})[position[x]] = facing
                else:
                    break
        else:
            if instruction == 'L':
                facing = facing - 1 if facing > 0 else 3
            else:
                facing = facing + 1 if facing < 3 else 0

        trace.setdefault(position[y], {})[position[x]] = facing
        # print(position)
        # log()

    print(position)
    return (1000 * position[y]) + (4 * position[x]) + facing


def part2(input: str, edges: Dict[Tuple[int, int, int], Tuple[int, int, int]]) -> int:
    y, x = 0, 1
    rows = {}
    columns = {}
    start = None
    path = []

    parse_path = False
    row = 1
    for line in input.split("\n"):
        if line == "":
            parse_path = True
            continue

        if parse_path:
            prev = None
            current = ""
            for char in line:
                if char.isnumeric() and prev is not None and not prev.isnumeric():
                    path.append(current)
                    current = char
                elif char.isalpha() and prev is not None and not prev.isalpha():
                    path.append(int(current))
                    current = char
                else:
                    current += char
                prev = char
        else:
            for i, char in enumerate(line):
                column = i + 1

                if start is None and char == ".":
                    start = [row, column]

                if char != ' ':
                    rows.setdefault(row, {}).setdefault(column, char)
                    columns.setdefault(column, {}).setdefault(row, char)

            row += 1

    path.append(int(current))

    bounds = (max(rows.keys()), max(columns.keys()))

    facings = (
        (0, 1),  # R
        (1, 0),  # D
        (0, -1),  # L
        (-1, 0),  # U
    )
    facing = 0

    position = start
    trace = {start[y]: {start[x]: facing}}

    def log():
        output = ""
        for row in range(1, bounds[y] + 1):
            line = ""
            for column in range(1, bounds[x] + 1):
                if [row, column] == position:
                    line += ["↦", "↧", "↤", "↥"][facing]
                elif row in trace and column in trace[row]:
                    line += [">", "v", "<", "^"][trace[row][column]]
                elif row in rows and column in rows[row]:
                    line += rows[row][column]
                else:
                    line += " "

            output += line + "\n"

        print(output)

    # print(position)
    # log()

    for instruction in path:
        # print(f"\n=== {instruction} ===\n")

        if type(instruction) == int:
            for _ in range(instruction):
                next_position = [position[y] + facings[facing][y], position[x] + facings[facing][x]]

                next_facing = None
                if rows.get(next_position[y], {}).get(next_position[x], None) is None:
                    try:
                        next_position[y], next_position[x], next_facing = edges[(position[y], position[x], facing)]
                        rows[next_position[y]][next_position[x]]
                    except KeyError:
                        log()
                        raise

                if rows[next_position[y]][next_position[x]] == '.':
                    position = next_position
                    if next_facing is not None:
                        facing = next_facing + 2
                        if facing > 3:
                            facing = facing % 2
                    trace.setdefault(position[y], {})[position[x]] = facing
                else:
                    break
        else:
            if instruction == 'L':
                facing = facing - 1 if facing > 0 else 3
            else:
                facing = facing + 1 if facing < 3 else 0

        trace.setdefault(position[y], {})[position[x]] = facing
        # print(position)
        # log()

    print(position)
    log()
    return (1000 * position[y]) + (4 * position[x]) + facing


def cube4_edges():
    cube = 4
    edges = {}
    for label, edge in {
        1: dict(zip([(y + 1, cube * 3, right) for y in range(cube)],
                    [(y + 1, cube * 4, right) for y in range(cube * 2, cube * 3)])),
        2: dict(zip([(y + 1, cube * 2 + 1, left) for y in range(cube)],
                    [(cube + 1, x + 1, up) for x in range(cube, cube * 2)])),
        3: dict(zip([(1, x + 1, up) for x in range(cube * 2, cube * 3)],
                    [(cube + 1, x + 1, up) for x in range(cube, 0, -1)])),
        4: dict(zip([(y, cube * 3, right) for y in range(cube * 2, cube - 1, -1)],
                    [(cube * 2 + 1, x + 1, up) for x in range(cube * 3, cube * 4)])),
        5: dict(zip([(cube * 2, x, down) for x in range(cube, 0, -1)],
                    [(cube * 3, x + 1, down) for x in range(cube * 2, cube * 3)])),
        6: dict(zip([(cube * 2, x + 1, down) for x in range(cube, cube * 2)],
                    [(cube * 2 + 1, y, left) for y in range(cube * 3, cube * 2, -1)])),
        7: dict(zip([(y + 1, 1, left) for y in range(cube, cube * 2)],
                    [(cube * 3, x + 1, down) for x in range(cube * 3, cube * 4)]))
    }.items():
        print(label, edge)
        edges.update(edge)
        edges.update({v: k for k, v in edge.items()})

    print(len(edges))
    return edges


def cube50_edges():
    cube = 50
    edges = {}
    for label, edge in {
        1: dict(zip([(cube, x + 1, down) for x in range(cube * 2, cube * 3)],
                    [(y + 1, cube * 2, right) for y in range(cube, cube * 2)])),
        2: dict(zip([(y, cube * 3, right) for y in range(cube, 0, -1)],
                    [(y + 1, cube * 2, right) for y in range(cube * 2, cube * 3)])),
        3: dict(zip([(y + 1, cube + 1, left) for y in range(cube, cube * 2)],
                    [(cube * 2 + 1, x + 1, up) for x in range(cube)])),
        4: dict(zip([(y + 1, cube + 1, left) for y in range(cube)],
                    [(y, 1, left) for y in range(cube * 3, cube * 2, -1)])),
        5: dict(zip([(1, x + 1, up) for x in range(cube, cube * 2)],
                    [(y + 1, 1, left) for y in range(cube * 3, cube * 4)])),
        6: dict(zip([(1, x + 1, up) for x in range(cube * 2, cube * 3)],
                    [(cube * 4, x + 1, down) for x in range(cube)])),
        7: dict(zip([(cube * 3, x + 1, down) for x in range(cube, cube * 2)],
                    [(y + 1, cube, right) for y in range(cube * 3, cube * 4)])),
    }.items():
        print(label, edge)
        edges.update(edge)
        edges.update({v: k for k, v in edge.items()})

    print(len(edges))
    return edges


class Test(unittest.TestCase):

    def test_part_1(self):
        self.assertEqual(6032, part1(Test.example))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        # self.assertEqual(5031, part2(Test.example, cube4_edges()))

        print(part2(Path('./input.txt').read_text(), cube50_edges()))

    example = """
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
""".strip("\n")
