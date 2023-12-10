import unittest
from inspect import cleandoc
from pathlib import Path
from typing import List, Mapping, Dict, Set, Tuple

from utils.neighbours import neighbours, DIRECTIONS_CARDINAL, Position, Direction, Grid

connections = {
    "|": {
        Direction.N: "|7F",
        Direction.S: "|JL"
    },
    "-": {
        Direction.E: "-J7",
        Direction.W: "-FL"
    },
    "F": {
        Direction.E: "-J7",
        Direction.S: "|JL"
    },
    "L": {
        Direction.E: "-J7",
        Direction.N: "|7F"
    },
    "J": {
        Direction.N: "|7F",
        Direction.W: "-FL"
    },
    "7": {
        Direction.S: "|JL",
        Direction.W: "-FL"
    }
}

corners = {
    "F": {
        Direction.N: Direction.E,
        Direction.W: Direction.S
    },
    "7": {
        Direction.E: Direction.S,
        Direction.N: Direction.W
    },
    "J": {
        Direction.E: Direction.N,
        Direction.S: Direction.W
    },
    "L": {
        Direction.S: Direction.E,
        Direction.W: Direction.N
    }
}


def parse(input: str) -> Grid:
    return tuple(tuple(line) for line in input.split("\n"))


def identify_loop(field: Grid) -> Tuple[List[Position], Dict[Position, Direction]]:
    S = (0, 0)

    for r, row in enumerate(field):
        for c, tile in enumerate(row):
            if tile == 'S':
                S = (r, c)

    loop: List[Position] = [S]
    heading: Dict[Position, Direction] = {}

    done = False
    while not done:
        head = loop[-1]
        tile = field[head[0]][head[1]]

        for (r, c), direction in neighbours(head, field, DIRECTIONS_CARDINAL):
            neighbour = field[r][c]

            if len(loop) == 1:
                if any(direction in valid and neighbour in valid[direction] for _, valid in connections.items()):
                    if r < head[0]:
                        heading[head] = Direction.N
                    if c > head[1]:
                        heading[head] = Direction.E
                    if r > head[0]:
                        heading[head] = Direction.S
                    if c < head[1]:
                        heading[head] = Direction.W

                    if neighbour in "|-":
                        heading[(r, c)] = heading[head]
                    else:
                        heading[(r, c)] = corners[neighbour][heading[head]]

                    loop.append((r, c))
                    break
                else:
                    continue

            if (r, c) == loop[-2]:
                continue

            if direction in connections[tile]:
                if (r, c) == S:
                    done = True
                    break

                if neighbour in connections[tile][direction]:
                    if neighbour in "|-":
                        heading[(r, c)] = heading[head]
                    else:
                        heading[(r, c)] = corners[neighbour][heading[head]]

                    loop.append((r, c))
                    break

    return loop, heading


def part1(input: str) -> int:
    loop, _ = identify_loop(input)

    i = 1
    j = len(loop) - 1

    while loop[i] != loop[j]:
        i += 1
        j -= 1

    return max(i, len(loop) - i)


def part2(input: str) -> int:
    field = parse(input)
    loop, heading = identify_loop(field)
    pipes = set(loop)

    visited: Set[Position] = set()

    queue: List[Position] = [(0, 0)]

    while len(queue):
        pos = queue.pop()

        if pos in visited:
            continue

        visited.add(pos)
        tile = field[pos[0]][pos[1]]

        print("\n".join(
            "".join(
                "x" if (r, c) == pos else "*" if (r, c) in visited else field[r][c] for c in range(len(field[0])))
            for r in range(len(field))), "\n"
        )

        for (r, c), direction in neighbours(pos, field, DIRECTIONS_CARDINAL):
            neighbour = field[r][c]

            if (r, c) in visited:
                continue

            # if tile is not in the loop and the neighbour is, we can follow the neighbouring pipe if it has a parallel neighbour
            # if we're in between pipes, we can continue in the direction we're heading if the next pipes in that direction are parallel

            # Can go N along left hand pipe if (r-1, c) head (N, S)
            # Can go NE to go N along right hand pipe if (r-1, c-1) head (N, S)
            # Can go NW if (r-1, c) and (r-1, c) have heading in (N, S)
            #
            # Can go NE if (r-1, c) and (r-1, c+1) have same heading
            #   or (r-1, c) and (r, c+1) have heading in (E, W)

            if ((c == 0 or c == len(field[0]) - 1) and direction in (Direction.N, Direction.S)) or \
                    ((r == 0 or r == len(field) - 1) and direction in (Direction.E, Direction.W)):
                queue.append((r, c))

            if pos in pipes and \
                    (direction in (Direction.N, Direction.S) and heading in (Direction.N, Direction.S)) or \
                    (direction in (Direction.E, Direction.W) and heading in (Direction.E, Direction.W)):
                continue

            # if pos in pipes and (r, c) not in pipes:
            #     if tile in "7JF|" and direction not in (Direction.N, Direction.S):
            #         continue
            #
            # if (r, c) not in pipes:
            #     queue.append((r, c))
            #     continue
            #
            # if (r, c) in pipes:
            #     if direction == Direction.N and c < len(field[r]) - 1 and \
            #             neighbour in ".|J7" and field[r][c + 1] in ".|LF":
            #         visited.add((r, c + 1))
            #         queue.append((r, c))

    print("\n".join(
        "".join("I" if (r, c) not in visited and (r, c) not in pipes else field[r][c] for c in
                range(len(field[0])))
        for r in range(len(field))), "\n"
    )

    return len(field) * len(field[0]) - len(pipes.union(visited))


box_drawing = {
    "|": "┃",
    "-": "━",
    "F": "┏",
    "7": "┓",
    "J": "┛",
    "L": "┗"
}

loop_closer = {
    ("┛", "┓"): "┏"
}


def print_example(input: str):
    field = parse(input)
    loop, heading = identify_loop(field)
    field = list(list(row) for row in field)

    for pos in loop:
        field[pos[0]][pos[1]] = box_drawing.get(field[pos[0]][pos[1]], "S")

    field[loop[0][0]][loop[0][1]] = loop_closer[(field[loop[-1][0]][loop[-1][1]], field[loop[1][0]][loop[1][1]])]

    print("\n".join("".join(row) for row in field), "\n")
    # print("\n".join("".join(heading[(r, c)].name if (r, c) in heading else field[r][c]
    #                         for c in range(len(field[0]))) for r in range(len(field))), "\n")


    expanded_loop = []
    expanded_heading = {}
    expanded_field = {}

    queue = loop.copy()
    r = 0
    c = 0
    dim = [[float('Inf'), float('Inf')], [float('-Inf'), float('-Inf')]]
    while len(queue):
        pos = queue.pop(0)
        tile = field[pos[0]][pos[1]]

        if tile == "┃":
            expanded_loop.append((r, c))
            expanded_heading[(r, c)] = heading[pos]
            expanded_field[(r, c)] = "┃"
            r += heading[pos].value[0]
            expanded_loop.append((r, c))
            expanded_heading[(r, c)] = heading[pos]
            expanded_field[(r, c)] = "┃"
            r += heading[pos].value[0]

        if tile == "━":
            expanded_loop.append((r, c))
            expanded_heading[(r, c)] = heading[pos]
            expanded_field[(r, c)] = "━"
            c += heading[pos].value[1]
            expanded_loop.append((r, c))
            expanded_heading[(r, c)] = heading[pos]
            expanded_field[(r, c)] = "━"
            c += heading[pos].value[1]

        if tile == "┏":
            if heading[pos] == Direction.E:
                expanded_loop.append((r, c))
                expanded_heading[(r, c)] = Direction.N
                expanded_field[(r, c)] = "┃"
                r -= 1
                expanded_loop.append((r, c))
                expanded_heading[(r, c)] = Direction.E
                expanded_field[(r, c)] = "┏"
                c += 1
                expanded_loop.append((r, c))
                expanded_heading[(r, c)] = Direction.E
                expanded_field[(r, c)] = "━"
                c += 1
            else:
                expanded_loop.append((r, c))
                expanded_heading[(r, c)] = Direction.W
                expanded_field[(r, c)] = "━"
                c -= 1
                expanded_loop.append((r, c))
                expanded_heading[(r, c)] = Direction.S
                expanded_field[(r, c)] = "┏"
                r += 1
                expanded_loop.append((r, c))
                expanded_heading[(r, c)] = Direction.S
                expanded_field[(r, c)] = "┃"
                r += 1

        if tile == "┓":
            if heading[pos] == Direction.S:
                expanded_loop.append((r, c))
                expanded_heading[(r, c)] = Direction.E
                expanded_field[(r, c)] = "━"
                c += 1
                expanded_loop.append((r, c))
                expanded_heading[(r, c)] = Direction.S
                expanded_field[(r, c)] = "┓"
                r += 1
                expanded_loop.append((r, c))
                expanded_heading[(r, c)] = Direction.S
                expanded_field[(r, c)] = "┃"
                r += 1
            else:
                expanded_loop.append((r, c))
                expanded_heading[(r, c)] = Direction.N
                expanded_field[(r, c)] = "┃"
                r -= 1
                expanded_loop.append((r, c))
                expanded_heading[(r, c)] = Direction.W
                expanded_field[(r, c)] = "┓"
                c -= 1
                expanded_loop.append((r, c))
                expanded_heading[(r, c)] = Direction.W
                expanded_field[(r, c)] = "━"
                c -= 1

        if tile == "┛":
            if heading[pos] == Direction.N:
                expanded_loop.append((r, c))
                expanded_heading[(r, c)] = Direction.E
                expanded_field[(r, c)] = "━"
                c += 1
                expanded_loop.append((r, c))
                expanded_heading[(r, c)] = Direction.N
                expanded_field[(r, c)] = "┛"
                r -= 1
                expanded_loop.append((r, c))
                expanded_heading[(r, c)] = Direction.N
                expanded_field[(r, c)] = "┃"
                r -= 1
            else:
                expanded_loop.append((r, c))
                expanded_heading[(r, c)] = Direction.S
                expanded_field[(r, c)] = "┃"
                r += 1
                expanded_loop.append((r, c))
                expanded_heading[(r, c)] = Direction.W
                expanded_field[(r, c)] = "┛"
                c -= 1
                expanded_loop.append((r, c))
                expanded_heading[(r, c)] = Direction.W
                expanded_field[(r, c)] = "━"
                c -= 1

        if tile == "┗":
            if heading[pos] == Direction.E:
                expanded_loop.append((r, c))
                expanded_heading[(r, c)] = Direction.S
                expanded_field[(r, c)] = "┃"
                r += 1
                expanded_loop.append((r, c))
                expanded_heading[(r, c)] = Direction.E
                expanded_field[(r, c)] = "┗"
                c += 1
                expanded_loop.append((r, c))
                expanded_heading[(r, c)] = Direction.E
                expanded_field[(r, c)] = "━"
                c += 1
            else:
                expanded_loop.append((r, c))
                expanded_heading[(r, c)] = Direction.W
                expanded_field[(r, c)] = "━"
                c -= 1
                expanded_loop.append((r, c))
                expanded_heading[(r, c)] = Direction.N
                expanded_field[(r, c)] = "┗"
                r -= 1
                expanded_loop.append((r, c))
                expanded_heading[(r, c)] = Direction.N
                expanded_field[(r, c)] = "┃"
                r -= 1

        if r < dim[0][0]:
            dim[0][0] = r
        if r > dim[1][0]:
            dim[1][0] = r
        if c < dim[0][1]:
            dim[0][1] = c
        if c > dim[1][1]:
            dim[1][1] = c

    debug = ""
    for i in range(dim[0][0] - 1 - 3, dim[1][0] + 2 + 3):
        for j in range(dim[0][1] - 1 - 3, dim[1][1] + 2 + 3):
            if (i, j) in expanded_loop:
                debug += expanded_field.get((i, j), '?')
            else:
                debug += "."

        debug += "\n"

    print(debug)



class Test(unittest.TestCase):
    example1 = cleandoc("""
        -L|F7
        7S-7|
        L|7||
        -L-J|
        L|-JF
    """)

    example2 = cleandoc("""
        7-F7-
        .FJ|7
        SJLL7
        |F--J
        LJ.LJ
    """)

    example3 = cleandoc("""
        ...........
        .S-------7.
        .|F-----7|.
        .||.....||.
        .||.....||.
        .|L-7.F-J|.
        .|..|.|..|.
        .L--J.L--J.
        ...........
    """)

    example4 = cleandoc("""
        ..........
        .S------7.
        .|F----7|.
        .||....||.
        .||....||.
        .|L-7F-J|.
        .|..||..|.
        .L--JL--J.
        ..........
    """)

    example5 = cleandoc("""
        .F----7F7F7F7F-7....
        .|F--7||||||||FJ....
        .||.FJ||||||||L7....
        FJL7L7LJLJ||LJ.L-7..
        L--J.L7...LJS7F-7L7.
        ....F-J..F7FJ|L7L7L7
        ....L7.F7||L7|.L7L7|
        .....|FJLJ|FJ|F7|.LJ
        ....FJL-7.||.||||...
        ....L---J.LJ.LJLJ...
    """)

    def test_part_1(self):
        self.assertEqual(4, part1(Test.example1))
        self.assertEqual(8, part1(Test.example2))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        # self.assertEqual(4, part2(Test.example3))
        # self.assertEqual(4, part2(Test.example4))
        print_example(Test.example5)
        # self.assertEqual(8, part2(Test.example5))

        # print(part2(Path('./input.txt').read_text()))
