import unittest
from collections import deque
from pathlib import Path


def part1(input: str) -> int:
    visits = {(0, 0)}
    head = (0, 0)
    tail = (0, 0)

    moves = {
        'R': (1, 0),
        'L': (-1, 0),
        'U': (0, 1),
        'D': (0, -1)
    }
    x = 0
    y = 1

    def log():
        return
        print()
        for i in range(4, -1, -1):
            print("".join(["H" if (j, i) == head else "T" if (j, i) == tail else "." for j in range(6)]))

    for motion in input.split("\n"):
        direction, steps = motion.split(" ")
        head_move = moves[direction]

        # print(f"\n== {motion} ==\n")

        for step in range(int(steps)):
            head = (head[x] + head_move[x], head[y] + head_move[y])

            distance = abs(head[x] - tail[x]) + abs(head[y] - tail[y])

            if distance < 2 and (tail[x] == head[x] or tail[y] == head[y]) or distance == 2 and tail[x] != head[x] and \
                    tail[y] != head[y]:
                log()
                continue

            for tail_move in [
                (0, 1),  # top
                (1, 1),  # top right
                (1, 0),  # right
                (1, -1),  # bottom right
                (0, -1),  # bottom
                (-1, -1),  # bottom left
                (-1, 0),  # left
                (-1, 1),  # top left
            ]:
                new_tail = (tail[x] + tail_move[x], tail[y] + tail_move[y])
                if abs(head[x] - new_tail[x]) + abs(head[y] - new_tail[y]) == 1:
                    tail = new_tail
                    visits.add(tail)
                    break

            log()

    return len(visits)


def part2(input: str, logger=None) -> int:
    start = logger["start_position"] if logger is not None else (0, 0)
    visits = {start}
    snake = [start for _ in range(10)]

    moves = {
        'R': (1, 0),
        'L': (-1, 0),
        'U': (0, 1),
        'D': (0, -1)
    }
    x = 0
    y = 1

    def log():
        if logger is None:
            return

        print()
        for i in range(logger["grid_size"][1] - 1, -1, -1):
            row = ""
            for j in range(logger["grid_size"][0]):
                if snake[0] == (j, i):
                    row += "H"
                    continue
                try:
                    row += str(snake.index((j, i)))
                except ValueError:
                    row += "."

            print(row)

    for motion in input.split("\n"):
        direction, steps = motion.split(" ")
        head_move = moves[direction]

        if logger:
            print(f"\n== {motion} ==")

        for step in range(int(steps)):
            snake[0] = (snake[0][x] + head_move[x], snake[0][y] + head_move[y])

            for i in range(1, 10):
                head = snake[i - 1]
                tail = snake[i]

                distance = abs(head[x] - tail[x]) + abs(head[y] - tail[y])

                if distance < 2 and (tail[x] == head[x] or tail[y] == head[y]) or \
                        distance == 2 and tail[x] != head[x] and tail[y] != head[y]:
                    break

                tail_move = (float('inf'), None)

                for tail_move_try in [
                    (0, 1),  # top
                    (1, 1),  # top right
                    (1, 0),  # right
                    (1, -1),  # bottom right
                    (0, -1),  # bottom
                    (-1, -1),  # bottom left
                    (-1, 0),  # left
                    (-1, 1),  # top left
                ]:
                    new_tail = (tail[x] + tail_move_try[x], tail[y] + tail_move_try[y])
                    new_distance = abs(head[x] - new_tail[x]) + abs(head[y] - new_tail[y])
                    if new_distance < tail_move[0]:
                        tail_move = (new_distance, tail_move_try)

                snake[i] = (snake[i][x] + tail_move[1][x], snake[i][y] + tail_move[1][y])

            visits.add(snake[9])

            if logger and logger["each_step"]:
                log()

        if logger and not logger["each_step"]:
            log()

    return len(visits)


class Test(unittest.TestCase):
    example = """
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
""".strip("\n")

    def test_part_1(self):
        self.assertEqual(13, part1(Test.example))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
#         self.assertEqual(1, part2(Test.example, {"grid_size": (6, 5), "start_position": (0, 0), "each_step": True}))
#         self.assertEqual(36, part2("""
# R 5
# U 8
# L 8
# D 3
# R 17
# D 10
# L 25
# U 20""".strip("\n"), {"grid_size": (26, 21), "start_position": (11, 5), "each_step": False}))

        print(part2(Path('./input.txt').read_text()))
