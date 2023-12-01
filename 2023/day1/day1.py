import unittest
from pathlib import Path


def part1(input: str) -> int:
    result = 0

    for line in input.split("\n"):
        a = None
        b = None

        for i in range(len(line)):
            try:
                a = int(line[i])
                break
            except ValueError:
                continue

        for j in range(len(line) - 1, -1, -1):
            try:
                b = int(line[j])
                break
            except ValueError:
                continue

        result += int(str(a) + str(b))

    return result


def part2(input: str) -> int:
    digits = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9
    }

    def get_digit(line, i):
        try:
            return int(line[i])
        except ValueError:
            pass

        for digit, value in digits.items():
            if line[i:i+len(digit)] == digit:
                return value

        return None

    result = 0

    for line in input.split("\n"):
        a = None
        b = None

        for i in range(len(line)):
            a = get_digit(line, i)
            if a is not None:
                break

        for j in range(len(line) - 1, -1, -1):
            b = get_digit(line, j)
            if b is not None:
                break

        result += int(str(a) + str(b))

    return result


class Test(unittest.TestCase):
    example1 = '\n'.join([
        "1abc2",
        "pqr3stu8vwx",
        "a1b2c3d4e5f",
        "treb7uchet",
    ])

    example2 = '\n'.join([
        "two1nine",
        "eightwothree",
        "abcone2threexyz",
        "xtwone3four",
        "4nineeightseven2",
        "zoneight234",
        "7pqrstsixteen",
    ])

    def test_part_1(self):
        self.assertEqual(142, part1(Test.example1))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(281, part2(Test.example2))

        print(part2(Path('./input.txt').read_text()))
