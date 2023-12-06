import unittest
from pathlib import Path


def part1(input: str) -> int:
    lines = input.split("\n")
    durations = list(map(int, filter(len, lines.pop(0)[len("Time:"):].split(" "))))
    records = list(map(int, filter(len, lines.pop(0)[len("Distance:"):].split(" "))))

    result = 1

    for i in range(len(durations)):
        duration = durations[i]
        record = records[i]

        wins = 0

        for t in range(duration):
            distance = (duration - t) * t
            if distance > record:
                wins += 1

        result *= wins

    return result


def part2(input: str) -> int:
    lines = input.split("\n")
    duration = int("".join(filter(len, lines.pop(0)[len("Time:"):].split(" "))))
    record = int("".join(filter(len, lines.pop(0)[len("Distance:"):].split(" "))))

    result = 0

    for t in range(duration):
        distance = (duration - t) * t
        if distance > record:
            result += 1

    return result


class Test(unittest.TestCase):
    example1 = '\n'.join([
        "Time:      7  15   30",
        "Distance:  9  40  200"
    ])

    def test_part_1(self):
        self.assertEqual(288, part1(Test.example1))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(71503, part2(Test.example1))

        print(part2(Path('./input.txt').read_text()))
