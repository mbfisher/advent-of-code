import unittest
from inspect import cleandoc
from pathlib import Path


def part1(input: str) -> int:
    result = 0

    for line in input.split("\n"):
        layers = [list(map(int, line.split(" ")))]

        while not all(diff == 0 for diff in layers[-1]):
            next_layer = []
            prev_layer = layers[-1]

            for i in range(1, len(prev_layer)):
                next_layer.append(prev_layer[i] - prev_layer[i - 1])

            layers.append(next_layer)

        prediction = 0
        for j in range(len(layers) - 1, -1, -1):
            prediction += layers[j][-1]

        result += prediction

    return result


def part2(input: str) -> int:
    result = 0

    for line in input.split("\n"):
        layers = [list(map(int, line.split(" ")))]

        while not all(diff == 0 for diff in layers[-1]):
            next_layer = []
            prev_layer = layers[-1]

            for i in range(1, len(prev_layer)):
                next_layer.append(prev_layer[i] - prev_layer[i - 1])

            layers.append(next_layer)

        # 5  10  13  16  21  30  45
        #   5   3   3   5   9  15
        #    -2   0   2   4   6
        #       2   2   2   2
        #       ^ 0 ^ 0   0
        #       | ^ |
        #       x c p
        # x = p - c
        # 2 = 2 - 0

        # 5  10  13  16  21  30  45
        #   5   3   3   5   9  15
        #    -2   0   2   4   6
        #     ^ 2 ^ 2   2   2
        #     | ^ |
        #     x c p
        # x = p - c
        # -2 = 0 - 2

        # 5  10  13  16  21  30  45
        #   5   3   3   5   9  15
        #   ^-2 ^ 0   2   4   6
        #   | ^ |
        #   x c p
        # x = p - c
        # 5 = 3 - -2

        for j in range(len(layers) - 2, -1, -1):
            layer = layers[j + 1]
            prev_layer = layers[j]
            value = prev_layer[0] - layer[0]
            prev_layer.insert(0, value)

        prediction = layers[0][0]
        result += prediction

    return result


class Test(unittest.TestCase):
    example1 = cleandoc("""
        0 3 6 9 12 15
        1 3 6 10 15 21
        10 13 16 21 30 45
    """)

    def test_part_1(self):
        self.assertEqual(114, part1(Test.example1))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(2, part2(Test.example1))

        print(part2(Path('./input.txt').read_text()))
