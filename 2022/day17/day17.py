import unittest
from collections import deque
from pathlib import Path
from typing import Set


class Chamber:

    def __init__(self, debug=False):
        self.debug = debug
        self.occupied = set()

    def tower_height(self):
        return max(y for (_, y) in self.occupied) + 1 if len(self.occupied) > 0 else 0

    def new_rock(self, rock_type) -> 'Rock':
        self.falling_rock = {
            "minus": MinusRock,
            "plus": PlusRock,
            "L": LRock,
            "I": IRock,
            "box": BoxRock,
        }[rock_type](self)

        self.print()
        return self.falling_rock

    def print(self, label=None):
        if not self.debug or label and self.debug != "all":
            return

        rows = []

        for y in range(-1, max(self.tower_height(), max(y for x, y in self.falling_rock.position)) + 1):
            if y == -1:
                rows.append('+-------+')
                continue

            line = []
            for x in range(-1, 8):
                if x == -1 or x == 7:
                    line.append("|")

                elif (x, y) in self.occupied:
                    line.append("#")

                elif (x, y) in self.falling_rock.position:
                    line.append("@")

                else:
                    line.append(".")

            rows.append("".join(line))

        if label:
            print(label)

        print("\n".join(reversed(rows)) + "\n")


class Rock:
    def __init__(self, chamber: Chamber):
        self.chamber = chamber

        self.position: Set[int] = set()
        self.landed = False

        self.start(2, chamber.tower_height() + 3)

    def start(self, left, bottom):
        raise

    def is_into_walls(self, next_position):
        return any(map(lambda p: p[0] < 0 or p[0] > 6, next_position))

    def is_into_floor(self, next_position):
        return any(map(lambda p: p[1] < 0, next_position))

    def is_into_rock(self, next_position):
        return len(self.chamber.occupied.intersection(next_position)) > 0

    def left(self):
        next_position = {(x - 1, y) for x, y in self.position}

        if not self.is_into_walls(next_position) and not self.is_into_rock(next_position):
            self.position = next_position

        self.chamber.print(label="left")

    def right(self):
        next_position = {(x + 1, y) for x, y in self.position}

        if not self.is_into_walls(next_position) and not self.is_into_rock(next_position):
            self.position = next_position

        self.chamber.print(label="right")

    def down(self):
        next_position = {(x, y - 1) for x, y in self.position}

        if not self.is_into_floor(next_position) and not self.is_into_rock(next_position):
            self.position = next_position
        else:
            self.chamber.occupied.update(self.position)
            self.landed = True

        self.chamber.print(label="down")


class MinusRock(Rock):
    def start(self, left, bottom):
        self.position = {(left + i, bottom) for i in range(4)}


class PlusRock(Rock):
    def start(self, left, bottom):
        self.position = {
            (left + 1, bottom + 2),
            (left, bottom + 1), (left + 1, bottom + 1), (left + 2, bottom + 1),
            (left + 1, bottom)
        }


class LRock(Rock):
    def start(self, left, bottom):
        self.position = {
            (left + 2, bottom + 2),
            (left + 2, bottom + 1),
            (left, bottom), (left + 1, bottom), (left + 2, bottom)
        }


class IRock(Rock):
    def start(self, left, bottom):
        self.position = {(left, bottom + i) for i in range(4)}


class BoxRock(Rock):
    def start(self, left, bottom):
        self.position = {
            (left, bottom + 1), (left + 1, bottom + 1),
            (left, bottom), (left + 1, bottom),
        }


def part1(input: str) -> int:
    jets = deque(input)
    rocks = deque(["minus", "plus", "L", "I", "box"])
    chamber = Chamber()

    for _ in range(2022):
        rock_type = rocks.popleft()
        rocks.append(rock_type)

        rock = chamber.new_rock(rock_type)

        while not rock.landed:
            jet = jets.popleft()
            jets.append(jet)

            if jet == ">":
                rock.right()
            elif jet == "<":
                rock.left()
            else:
                raise

            rock.down()

    return chamber.tower_height()


def part2(input: str) -> int:
    jets = deque(input)
    rocks = deque(["minus", "plus", "L", "I", "box"])
    chamber = Chamber()

    for i in range(1000000000000):
        if i % 1000 == 0:
            print(i)

        rock_type = rocks.popleft()
        rocks.append(rock_type)

        rock = chamber.new_rock(rock_type)

        while not rock.landed:
            jet = jets.popleft()
            jets.append(jet)

            if jet == ">":
                rock.right()
            elif jet == "<":
                rock.left()
            else:
                raise

            rock.down()

        height = chamber.tower_height()
        if height % 2 > 0:
            continue

        halves = (
            {(x, y) for x, y in chamber.occupied if y < height//2},
            {(x, y-height//2) for x, y in chamber.occupied if y >= height//2},
        )

        if halves[0] == halves[1]:
            print("cycle!")
            return

    return chamber.tower_height()


class Test(unittest.TestCase):

    def test_part_1(self):
        self.assertEqual(3068, part1(Test.example))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(1514285714288, part2(Test.example))

        # print(part2(Path('./input.txt').read_text()))

    example = """
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
""".strip("\n")
