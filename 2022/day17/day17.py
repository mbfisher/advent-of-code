import unittest
from collections import deque
from pathlib import Path
from typing import Set


class Chamber:

    def __init__(self, debug=False):
        self.debug = debug
        self.columns = {i: set() for i in range(7)}
        self.heights = {i: 0 for i in range(7)}

    def tower_height(self):
        return max(self.heights.values())

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

                elif y in self.columns[x]:
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
        for x, y in next_position:
            if y in self.chamber.columns[x]:
                return True

        return False

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
            for x, y in self.position:
                self.chamber.columns[x].add(y)
                if y + 1 > self.chamber.heights[x]:
                    self.chamber.heights[x] = y + 1
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
    jets = list(input)
    jet_index = 0
    rocks = ["minus", "plus", "L", "I", "box"]
    chamber = Chamber()
    states = {}
    cycle_found = False
    height_increase = 0

    rock_count = 0
    while rock_count < 1000000000000:
        rock_count += 1
        rock_type = rocks[(rock_count - 1) % 5]
        rock = chamber.new_rock(rock_type)

        while not rock.landed:
            jet = jets[jet_index]
            jet_index += 1
            if jet_index >= len(jets):
                jet_index = 0

            if jet == ">":
                rock.right()
            elif jet == "<":
                rock.left()
            else:
                raise

            rock.down()

        if cycle_found:
            continue

        height = chamber.tower_height()

        state_key = []

        min_column = min(h for h in chamber.heights.values() if h > 0)
        for column_height in chamber.heights.values():
            state_key.append(column_height - min_column if column_height > 0 else -1)

        state_key.extend([rock_type, jet_index])
        state_key = tuple(state_key)

        if state_key in states:
            print("cycle!", rock_count)
            cycle_found = True

            prev_state = states[state_key]

            cycle_rock_count = rock_count - prev_state["rock_count"]
            cycle_height = height - prev_state["height"]

            rocks_remaining = 1000000000000 - rock_count
            cycles_remaining = rocks_remaining // cycle_rock_count

            rock_count += cycles_remaining * cycle_rock_count
            height_increase = cycle_height * cycles_remaining
        else:
            states[state_key] = {
                'rock_count': rock_count,
                'height': height
            }

    return chamber.tower_height() + height_increase


class Test(unittest.TestCase):

    def test_part_1(self):
        self.assertEqual(3068, part1(Test.example))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(1514285714288, part2(Test.example))

        print(part2(Path('./input.txt').read_text()))

    example = """
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
""".strip("\n")
