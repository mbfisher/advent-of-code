import unittest
from pathlib import Path

turn_right = {
    (-1, 0): (0, 1),
    (0, 1): (1, 0),
    (1, 0): (0, -1),
    (0, -1): (-1, 0),
}

pointers = {
    (-1, 0): '^',
    (0, 1): '>',
    (1, 0): 'v',
    (0, -1): '<',
}

def part1(input: str, debug=False) -> int:
    lab = list(map(list, input.splitlines()))
    pos = next((i, row.index('^')) for i, row in enumerate(lab) if '^' in row)
    move = (-1, 0)
    positions = {pos}

    while 0 <= pos[0] + move[0] < len(lab) and 0 <= pos[1] + move[1] < len(lab[0]):
        if debug:
            print("\n".join(
                "".join(pointers[move] if (i, j) == pos else char for j, char in enumerate(line))
                for i, line in enumerate(lab)
            ) + "\n")

        if lab[pos[0] + move[0]][pos[1] + move[1]] == '#':
            move = turn_right[move]
        else:
            pos = (pos[0] + move[0], pos[1] + move[1])
            positions.add(pos)

    return len(positions)


def part2(input: str, debug=False) -> int:
    lab = list(map(list, input.splitlines()))
    start = next((i, row.index('^')) for i, row in enumerate(lab) if '^' in row)
    obstructions = set()

    for i in range(len(lab)):
        for j in range(len(lab[0])):
            obs = (i, j)
            if obs == start:
                continue

            pos = start
            move = (-1, 0)
            positions = {pos: {move}}

            while 0 <= pos[0] + move[0] < len(lab) and 0 <= pos[1] + move[1] < len(lab[0]):
                positions.setdefault(pos, set()).add(move)
                next_pos = (pos[0] + move[0], pos[1] + move[1])

                if lab[next_pos[0]][next_pos[1]] == '#' or next_pos == obs:
                    move = turn_right[move]
                else:
                    pos = next_pos

                if pos in positions and move in positions[pos]:
                    obstructions.add(obs)

                    if debug:
                        print(obs)

                        output = lab.copy()
                        output[start[0]][start[1]] = '^'
                        output[obs[0]][obs[1]] = 'O'

                        for (r, c), moves in positions.items():
                            if (r, c) == start:
                                continue

                            if len(moves) == 1:
                                output[r][c] = '|' if moves.pop()[1] == 0 else '-'
                            else:
                                if all(map(lambda move: move[1] == 0, moves)):
                                    output[r][c] = '|'
                                elif all(map(lambda move: move[0] == 0, moves)):
                                    output[r][c] = '-'
                                else:
                                    output[r][c] = '+'

                        print("\n".join(map(lambda row: "".join(row), output)) + "\n")
                    break

    return len(obstructions)


class Test(unittest.TestCase):
    example1 = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
    """.strip()

    def test_part_1(self):
        self.assertEqual(41, part1(Test.example1, debug=False))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(6, part2(Test.example1, debug=True))

        print(part2(Path('./input.txt').read_text()))
