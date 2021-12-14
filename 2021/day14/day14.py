from __future__ import annotations

from itertools import chain
from pathlib import Path
from typing import Tuple, List, Dict, Set


class Polymer:
    def __init__(self, input: str):
        lines = input.splitlines()
        self.template: List[str] = list(lines.pop(0))
        lines.pop(0)

        self.instructions: Dict[str, str] = {}
        for line in lines:
            pair, element = line.split(" -> ")
            self.instructions[pair] = element

    def next(self):
        pairs: List[List[str]] = [[self.template[i], self.template[i + 1]] for i in range(0, len(self.template) - 1)]

        for i, pair in enumerate(pairs):
            element = self.instructions.get(''.join(pair))
            if element:
                if i == len(pairs) - 1:
                    pair.insert(1, element)
                else:
                    pair[1] = element
            else:
                pair.pop()

        self.template = list(chain.from_iterable(pairs))

        result = ''.join(self.template)
        return result


def part1(input: str, steps=10) -> int:
    polymer = Polymer(input)
    result = None
    for i in range(0, steps):
        result = polymer.next()

    elements: Dict[str, int] = {}
    for element in result:
        elements.setdefault(element, 0)
        elements[element] += 1

    occurrences = sorted(elements.values())
    return occurrences[-1] - occurrences[0]


class Polymer2:
    def __init__(self, input: str):
        lines = input.splitlines()
        template: List[str] = list(lines.pop(0))
        lines.pop(0)

        self.instructions: Dict[str, str] = {}
        for line in lines:
            pair, element = line.split(" -> ")
            self.instructions[pair] = element

        self.pairs: Dict[str, int] = {}

        for i in range(0, len(template) - 1):
            pair = template[i] + template[i + 1]
            self.pairs.setdefault(pair, 0)
            self.pairs[pair] += 1

        self.elements: Dict[str, int] = {}
        for element in template:
            self.elements.setdefault(element, 0)
            self.elements[element] += 1

    def next(self):
        next_pairs: Dict[str, int] = {}

        for pair, count in self.pairs.items():
            insertion = self.instructions.get(pair)
            if insertion:
                for new_pair in [pair[0] + insertion, insertion + pair[1]]:
                    next_pairs.setdefault(new_pair, 0)
                    next_pairs[new_pair] += count

                self.elements.setdefault(insertion, 0)
                self.elements[insertion] += count

        self.pairs = {pair: count for pair, count in next_pairs.items() if count > 0}
        # print('got', [f'{pair}={self.pairs[pair]}' for pair in sorted(list(self.pairs.keys()))])
        return self.pairs


def part2(input: str, steps=10) -> int:
    polymer = Polymer2(input)
    result = None
    for i in range(0, steps):
        result = polymer.next()

    # {'N': 865, 'B': 1749, 'C': 298, 'H': 161}
    occurrences = sorted(polymer.elements.values())
    return occurrences[-1] - occurrences[0]


if __name__ == '__main__':
    example = '\n'.join([
        "NNCB",
        "",
        "CH -> B",
        "HH -> N",
        "CB -> H",
        "NH -> C",
        "HB -> C",
        "HC -> B",
        "HN -> C",
        "NN -> C",
        "BH -> H",
        "NC -> B",
        "NB -> B",
        "BN -> B",
        "BB -> N",
        "BC -> B",
        "CC -> N",
        "CN -> C",
    ])

    input = Path('./input.txt').read_text()

    polymer = Polymer(example)
    assert polymer.next() == "NCNBCHB"
    assert polymer.next() == "NBCCNBBBCBHCB"
    assert polymer.next() == "NBBBCNCCNBBNBNBBCHBHHBCHB"
    assert polymer.next() == "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB"

    example_part1 = part1(example)
    assert example_part1 == 1588, f"got {example_part1}"
    print(part1(input))


    def count_pairs(template):
        result = {}
        for i in range(0, len(template) - 1):
            pair = template[i] + template[i + 1]
            result.setdefault(pair, 0)
            result[pair] += 1

        # print('want', [f'{pair}={result[pair]}' for pair in sorted(list(result.keys()))])
        return result


    polymer2 = Polymer2(example)
    assert polymer2.next() == count_pairs("NCNBCHB")
    assert polymer2.next() == count_pairs("NBCCNBBBCBHCB")
    assert polymer2.next() == count_pairs("NBBBCNCCNBBNBNBBCHBHHBCHB")
    assert polymer2.next() == count_pairs("NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB")

    example_part2 = part2(example)
    assert example_part2 == 1588, f"got {example_part2}"

    print(part2(input, 40))
