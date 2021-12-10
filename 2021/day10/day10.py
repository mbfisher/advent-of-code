from __future__ import annotations

from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional

import math

chars = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}


class CorruptChunkError(Exception):
    values = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137
    }

    def __init__(self, expected, found):
        self.message = f"Expected {expected}, but found {found} instead"
        self.value = self.values[found]
        super().__init__(self.message)


def parse_chunk(chunk: str):
    stack = []

    for char in chunk:
        if char not in chars:
            # must be close
            if char != stack[-1]:
                raise CorruptChunkError(stack[-1], char)

            stack.pop()
        else:
            stack.append(chars[char])

    return stack


def part1(input: str) -> int:
    result = 0

    for chunk in input.splitlines():
        try:
            parse_chunk(chunk)
        except CorruptChunkError as e:
            result += e.value

    return result


def complete_chunk(chunk: str):
    stack = parse_chunk(chunk)
    stack.reverse()
    return ''.join(stack)


completion_scores = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}


def part2(input: str) -> int:
    scores = []
    for chunk in input.splitlines():
        try:
            fix = complete_chunk(chunk)
        except CorruptChunkError:
            continue

        score = 0
        for char in fix:
            score *= 5
            score += completion_scores[char]
        scores.append(score)

    scores.sort()
    return scores[int(len(scores) / 2)]


if __name__ == '__main__':
    example = '\n'.join([
        "[({(<(())[]>[[{[]{<()<>>",
        "[(()[<>])]({[<{<<[]>>(",
        "{([(<{}[<>[]}>{[]{[(<()>",
        "(((({<>}<{<{<>}{[]{[]{}",
        "[[<[([]))<([[{}[[()]]]",
        "[{[{({}]{}}([{[{{{}}([]",
        "{<[[]]>}<{[{[{[]{()[[[]",
        "[<(<(<(<{}))><([]([]()",
        "<{([([[(<>()){}]>(<<{{",
        "<{([{{}}[<[[[<>{}]]]>[]]",
    ])

    assert len(parse_chunk("()")) == 0
    assert len(parse_chunk("[]")) == 0
    assert len(parse_chunk("([])")) == 0
    assert len(parse_chunk("{()()()}")) == 0
    assert len(parse_chunk("<([{}])>")) == 0

    input = Path('./input.txt').read_text()

    example_part1 = part1(example)
    assert example_part1 == 26397, f"got {example_part1}"
    print(part1(input))

    assert complete_chunk("[({(<(())[]>[[{[]{<()<>>") == "}}]])})]"

    example_part2 = part2(example)
    assert example_part2 == 288957, f"got {example_part2}"
    print(part2(input))
