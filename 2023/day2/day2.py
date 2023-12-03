import unittest
from pathlib import Path


def part1(input: str) -> int:
    result = 0

    for line in input.split("\n"):
        info, game = line.split(": ", 1)
        game_id = int(info[5:])

        possible = True

        for reveal in game.split("; "):
            for spec in reveal.split(", "):
                number, colour = spec.split(" ")

                if colour == "red" and int(number) > 12:
                    possible = False

                if colour == "green" and int(number) > 13:
                    possible = False

                if colour == "blue" and int(number) > 14:
                    possible = False

        if possible:
            result += game_id

    return result

def part2(input: str) -> int:
    result = 0

    for line in input.split("\n"):
        info, game = line.split(": ", 1)
        game_id = int(info[5:])

        cubes = {}

        for reveal in game.split("; "):
            for spec in reveal.split(", "):
                number, colour = spec.split(" ")

                if colour not in cubes or int(number) > cubes[colour]:
                    cubes[colour] = int(number)

        result += cubes["red"] * cubes["green"] * cubes["blue"]

    return result


class Test(unittest.TestCase):
    example1 = '\n'.join([
        "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
        "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
        "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
        "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
        "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
    ])

    def test_part_1(self):
        self.assertEqual(8, part1(Test.example1))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(2286, part2(Test.example1))

        print(part2(Path('./input.txt').read_text()))
