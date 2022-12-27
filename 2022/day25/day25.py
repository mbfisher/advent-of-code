import unittest
from collections import deque
from pathlib import Path


def snafu_to_decimal(snafu: str) -> int:
    result = 0
    for i, char in enumerate(reversed(snafu)):
        if char == '-':
            digit = -1
        elif char == '=':
            digit = -2
        else:
            digit = int(char)

        result += digit * (5 ** i)

    return result


def decimal_to_snafu(decimal: int) -> str:
    if decimal <= 2:
        return str(decimal)

    digits = {
        -2: "=",
        -1: "-",
        0: "0",
        1: "1",
        2: "2",
    }
    ops = {
        0: 0,
        1: 1,
        2: 2,
        3: -2,
        4: -1
    }

    p = 0
    while sum(2 * 5 ** i for i in range(p + 1)) < decimal:
        p += 1

    result = ""
    value = decimal
    while p >= 0:
        r, d, _ = min(list((i * (5 ** p), d, abs(value - i * (5 ** p))) for i, d in digits.items()), key=lambda x: x[2])
        result += d
        value -= r
        p -= 1

    return result


def part1(input: str) -> str:
    result = sum(map(snafu_to_decimal, input.split("\n")))
    return decimal_to_snafu(result)


def part2(input: str) -> int:
    pass


class Test(unittest.TestCase):

    def test_part_1(self):
        self.assertEqual(10, snafu_to_decimal("20"))
        self.assertEqual(8, snafu_to_decimal("2="))
        self.assertEqual(976, snafu_to_decimal("2=-01"))

        self.assertEqual([
            "1",
            "2",
            "1=",
            "1-",
            "10",
            "11",
            "12",
            "2=",
            "2-",
            "20",
            "1=0",
            "1-0",
            "1=11-2",  # 2 -(1*5) +25 +125 -(2*265) +3125
            "1-0---0",
            "1121-1110-1=0"
        ], list(map(decimal_to_snafu, [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            15,
            20,
            2022,
            12345,
            314159265
        ])))

        self.assertEqual([
            1747,
            906,
            198,
            11,
            201,
            31,
            1257,
            32,
            353,
            107,
            7,
            3,
            37
        ], list(map(snafu_to_decimal, [
            "1=-0-2",
            "12111",
            "2=0=",
            "21",
            "2=01",
            "111",
            "20012",
            "112",
            "1=-1=",
            "1-12",
            "12",
            "1=",
            "122"
        ])))

        self.assertEqual("2=-1=0", part1(Test.example))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(54, part2(Test.example2))

        print(part2(Path('./input.txt').read_text()))

    example = """
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
""".strip("\n")