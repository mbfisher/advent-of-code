import unittest
from pathlib import Path


def part1(input: str) -> int:
    # A for Rock, B for Paper, and C for Scissors
    # X for Rock, Y for Paper, and Z for Scissors
    hands = {
        "A": "Rock",
        "B": "Paper",
        "C": "Scissors",
        "X": "Rock",
        "Y": "Paper",
        "Z": "Scissors",
    }

    # 1 for Rock, 2 for Paper, and 3 for Scissors
    # 0 if you lost, 3 if the round was a draw, and 6 if you won
    scores = {
        ("Rock", "Paper"): 8,
        ("Rock", "Scissors"): 3,
        ("Paper", "Rock"): 1,
        ("Paper", "Scissors"): 9,
        ("Scissors", "Rock"): 7,
        ("Scissors", "Paper"): 2,
        ("Rock", "Rock"): 4,
        ("Paper", "Paper"): 5,
        ("Scissors", "Scissors"): 6
    }

    score = 0
    for round in input.split("\n"):
        opponent, me = [hands[letter] for letter in round.split(" ")]

        round_score = scores[(opponent, me)]
        score += round_score

    return score


def part2(input: str) -> int:
    # A for Rock, B for Paper, and C for Scissors
    # X for Lose, Y for Draw, and Z for Win
    hands = {
        "A": "Rock",
        "B": "Paper",
        "C": "Scissors",
        "X": "Lose",
        "Y": "Draw",
        "Z": "Win",
    }

    # 1 for Rock, 2 for Paper, and 3 for Scissors
    # 0 if you lost, 3 if the round was a draw, and 6 if you won
    scores = {
        ("Rock", "Lose"): 3,  # Scissors
        ("Rock", "Win"): 8,  # Paper
        ("Rock", "Draw"): 4,  # Rock
        ("Paper", "Lose"): 1,  # Rock
        ("Paper", "Win"): 9,  # Scissors
        ("Paper", "Draw"): 5,  # Paper
        ("Scissors", "Lose"): 2,  # Paper
        ("Scissors", "Win"): 7,  # Rock
        ("Scissors", "Draw"): 6,  # Scissors
    }

    score = 0
    for round in input.split("\n"):
        opponent, me = [hands[letter] for letter in round.split(" ")]

        round_score = scores[(opponent, me)]
        score += round_score

    return score


class Test(unittest.TestCase):
    example = '\n'.join([
        "A Y",
        "B X",
        "C Z",
    ])

    def test_part_1(self):
        self.assertEqual(15, part1(Test.example))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(12, part2(Test.example))

        print(part2(Path('./input.txt').read_text()))
