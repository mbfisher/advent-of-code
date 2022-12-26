import unittest
from collections import deque
from pathlib import Path


def part1(input: str) -> int:
    start = None
    end = None
    blizzards = {}
    directions = ["^", "v", "<", ">"]
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    up, down, left, right = range(4)

    lines = input.split("\n")
    width = len(lines[0])
    height = len(lines)

    for row, line in enumerate(lines):
        if row == 0:
            start = (0, line.index("."))
            continue
        if row == len(lines) - 1:
            end = (height - 1, line.index("."))
            continue

        for column, char in enumerate(line):
            if char != "#" and char != ".":
                blizzards.setdefault((row, column), set()).add(char)

    def log():
        output = ""
        for row in range(height):
            for column in range(width):
                if (row, column) == start or (row, column) == end:
                    output += "."
                elif row == 0 or row == height - 1 or column == 0 or column == width - 1:
                    output += "#"
                elif (row, column) in blizzards:
                    position_blizzards = blizzards[(row, column)]
                    if len(position_blizzards) == 1:
                        output += next(iter(position_blizzards))
                    else:
                        output += str(len(position_blizzards))
                else:
                    output += "."
            output += "\n"
        print(output)

    # log()
    paths = {start: [start]}
    minute = 0
    result = None
    while result is None:
        minute += 1
        next_blizzards = {}
        for position, position_blizzards in blizzards.items():
            for blizzard in position_blizzards:
                move = moves[directions.index(blizzard)]
                next_position = [position[0] + move[0], position[1] + move[1]]
                if next_position[0] == 0 and blizzard == "^":
                    next_position[0] = height - 2
                elif next_position[0] == height - 1 and blizzard == "v":
                    next_position[0] = 1
                elif next_position[1] == 0 and blizzard == "<":
                    next_position[1] = width - 2
                elif next_position[1] == width - 1 and blizzard == ">":
                    next_position[1] = 1

                next_blizzards.setdefault(tuple(next_position), set()).add(blizzard)

        blizzards = next_blizzards

        elves = list(paths.keys())
        for elf in elves:
            path = paths.pop(elf)

            if elf not in blizzards:
                paths[elf] = path + [elf]

            for move in moves:
                next_position = (elf[0] + move[0], elf[1] + move[1])

                if next_position == end:
                    result = path + [next_position]
                    break

                if next_position[0] <= 0 or next_position[0] >= height - 1 \
                        or next_position[1] <= 0 or next_position[1] >= width - 1:
                    continue

                if next_position not in blizzards and (
                        next_position not in paths or len(paths[next_position]) > len(path) + 1):
                    paths[next_position] = path + [next_position]

        # print(minute, len(paths))
        # log()

    # blizzards = {}
    # for row, line in enumerate(lines):
    #     if row == 0:
    #         start = (0, line.index("."))
    #         continue
    #     if row == len(lines) - 1:
    #         end = (height - 1, line.index("."))
    #         continue
    #
    #     for column, char in enumerate(line):
    #         if char != "#" and char != ".":
    #             blizzards.setdefault((row, column), set()).add(char)
    #
    # log()
    # (0, 0, 1), (1, 1, 1), (2, 2, 1), (3, 2, 1), (4, 1, 1), (5, 1, 2), (6, 1, 3), (7, 2, 3),
    # (8, 2, 2), (9, 1, 2), (10, 1, 3), (11, 1, 3), (12, 2, 3), (13, 3, 3), (14, 3, 4), (15, 3, 5),
    # (16, 3, 6), (17, 4, 6), (18, 5, 6)
    # for minute, elf in enumerate(result):
    #     print(minute)
    #
    #     if elf in blizzards:
    #         raise
    #
    #     output = ""
    #     for row in range(height):
    #         for column in range(width):
    #             if (row, column) == elf:
    #                 output += "E"
    #             elif (row, column) == start or (row, column) == end:
    #                 output += "."
    #             elif row == 0 or row == height - 1 or column == 0 or column == width - 1:
    #                 output += "#"
    #             elif (row, column) in blizzards:
    #                 position_blizzards = blizzards[(row, column)]
    #                 if len(position_blizzards) == 1:
    #                     output += next(iter(position_blizzards))
    #                 else:
    #                     output += str(len(position_blizzards))
    #             else:
    #                 output += "."
    #         output += "\n"
    #     print(output)
    #
    #     next_blizzards = {}
    #     for position, position_blizzards in blizzards.items():
    #         for blizzard in position_blizzards:
    #             move = moves[directions.index(blizzard)]
    #             next_position = [position[0] + move[0], position[1] + move[1]]
    #             if next_position[0] == 0 and blizzard == "^":
    #                 next_position[0] = height - 2
    #             elif next_position[0] == height - 1 and blizzard == "v":
    #                 next_position[0] = 1
    #             elif next_position[1] == 0 and blizzard == "<":
    #                 next_position[1] = width - 2
    #             elif next_position[1] == width - 1 and blizzard == ">":
    #                 next_position[1] = 1
    #
    #             next_blizzards.setdefault(tuple(next_position), set()).add(blizzard)
    #
    #     blizzards = next_blizzards

    return len(result) - 1


def part2(input: str) -> int:
    start = None
    end = None
    blizzards = {}
    directions = ["^", "v", "<", ">"]
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    up, down, left, right = range(4)

    lines = input.split("\n")
    width = len(lines[0])
    height = len(lines)

    for row, line in enumerate(lines):
        if row == 0:
            start = (0, line.index("."))
            continue
        if row == len(lines) - 1:
            end = (height - 1, line.index("."))
            continue

        for column, char in enumerate(line):
            if char != "#" and char != ".":
                blizzards.setdefault((row, column), set()).add(char)

    paths = {start: [start]}
    targets = deque([end, start, end])
    target = None
    minute = 0
    while len(targets) or target:
        if target is None:
            target = targets.popleft()

        minute += 1
        next_blizzards = {}
        for position, position_blizzards in blizzards.items():
            for blizzard in position_blizzards:
                move = moves[directions.index(blizzard)]
                next_position = [position[0] + move[0], position[1] + move[1]]
                if next_position[0] == 0 and blizzard == "^":
                    next_position[0] = height - 2
                elif next_position[0] == height - 1 and blizzard == "v":
                    next_position[0] = 1
                elif next_position[1] == 0 and blizzard == "<":
                    next_position[1] = width - 2
                elif next_position[1] == width - 1 and blizzard == ">":
                    next_position[1] = 1

                next_blizzards.setdefault(tuple(next_position), set()).add(blizzard)

        blizzards = next_blizzards

        elves = list(paths.keys())
        for elf in elves:
            if target is None:
                break

            path = paths.pop(elf)

            if elf not in blizzards:
                paths[elf] = path + [elf]

            for move in moves:
                next_position = (elf[0] + move[0], elf[1] + move[1])

                if next_position == target:
                    paths = {target: path + [next_position]}
                    target = None
                    break

                if next_position[0] <= 0 or next_position[0] >= height - 1 \
                        or next_position[1] <= 0 or next_position[1] >= width - 1:
                    continue

                if next_position not in blizzards and (
                        next_position not in paths or len(paths[next_position]) > len(path) + 1):
                    paths[next_position] = path + [next_position]

    return len(paths[end]) - 1


class Test(unittest.TestCase):

    def test_part_1(self):
        # part1(Test.example1)
        self.assertEqual(18, part1(Test.example2))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(54, part2(Test.example2))

        print(part2(Path('./input.txt').read_text()))

    example1 = """
#.#####
#.....#
#>....#
#.....#
#...v.#
#.....#
#####.#
""".strip("\n")

    example2 = """
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
""".strip("\n")
