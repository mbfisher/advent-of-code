import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, TypedDict, Dict, Set, Tuple, Optional


class Card:
    def __init__(self) -> None:
        self.lines: List[List[int]] = []
        self.numbers: Dict[int, Tuple[int, int]] = {}
        self.marked: Set[int] = set()

    def add_row(self, row: List[int]):
        self.lines.append(row)

        row_index = len(self.lines) - 1
        for col_index, number in enumerate(row):
            self.numbers[number] = (row_index, col_index)

    def call_number(self, number: int) -> bool:
        if number not in self.numbers:
            return False

        self.marked.add(number)

        rows = self.lines

        line_len = len(self.lines)
        cols = [[self.lines[row_index][col_index] for row_index in range(0, line_len)] for col_index in
                range(0, line_len)]

        if any(all(number in self.marked for number in row) for row in rows):
            return True

        if any(all(number in self.marked for number in col) for col in cols):
            return True

        return False

    def score(self, number: int) -> int:
        unmarked = set([number for number, _ in self.numbers.items()]).difference(self.marked)
        return sum(unmarked) * number


def part1(input: str) -> int:
    lines = input.splitlines()

    numbers = lines.pop(0).split(",")
    lines.pop(0)

    cards: List[Card] = []
    card = Card()

    while len(lines) > 0:
        line = lines.pop(0)

        if line == "":
            cards.append(card)
            card = Card()
        else:
            try:
                card.add_row([int(number.strip()) for number in re.split('\s+', line) if number != ''])
            except ValueError:
                print(line)
                raise

    cards.append(card)

    winner: Optional[Card] = None

    for number in numbers:
        for card in cards:
            if card.call_number(int(number)):
                winner = card
                break

        if winner:
            break

    return winner.score(int(number))


def part2(input: str) -> int:
    lines = input.splitlines()

    numbers = lines.pop(0).split(",")
    lines.pop(0)

    cards: List[Card] = []
    card = Card()

    while len(lines) > 0:
        line = lines.pop(0)

        if line == "":
            cards.append(card)
            card = Card()
        else:
            try:
                card.add_row([int(number.strip()) for number in re.split('\s+', line) if number != ''])
            except ValueError:
                print(line)
                raise

    cards.append(card)

    winner: Optional[Card] = None
    players = cards
    winners = [False for _ in cards]

    for number in numbers:
        for i, card in enumerate(players):
            if card.call_number(int(number)):
                winners[cards.index(card)] = True
                winner = card

        players = [cards[i] for i, won in enumerate(winners) if not won]
        if len(players) == 0:
            break

    return winner.score(int(number))


if __name__ == '__main__':
    example = '\n'.join([
        "7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1",
        "",
        "22 13 17 11  0",
        "8  2 23  4 24",
        "21  9 14 16  7",
        "6 10  3 18  5",
        "1 12 20 15 19",
        "",
        "3 15  0  2 22",
        "9 18 13 17  5",
        "19  8  7 25 23",
        "20 11 10 24  4",
        "14 21 16 12  6",
        "",
        "14 21 17 24  4",
        "10 16 15  9 19",
        "18  8 23 26 20",
        "22 11 13  6  5",
        "2  0 12  3  7",
    ])

    input = Path('./input.txt').read_text()

    example_part1 = part1(example)
    assert example_part1 == 4512, f"got {example_part1}"
    print(part1(input))

    example_part2 = part2(example)
    assert example_part2 == 1924, f"got {example_part2}"
    print(part2(input))
