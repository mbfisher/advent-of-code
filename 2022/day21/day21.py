import unittest
from collections import deque
from pathlib import Path


def part1(input: str) -> int:
    monkeys = {}
    for line in input.split("\n"):
        name, job = line.split(": ")
        try:
            monkeys[name] = int(job)
        except ValueError:
            monkeys[name] = job.split(" ")

    while not all(type(job) == int for job in monkeys.values()):
        for name, job in monkeys.items():
            if type(job) == int:
                continue

            try:
                a, op, b = job
            except TypeError:
                raise

            if type(monkeys[a]) == int and type(monkeys[b]) == int:
                if op == "+":
                    monkeys[name] = monkeys[a] + monkeys[b]
                if op == "-":
                    monkeys[name] = monkeys[a] - monkeys[b]
                if op == "*":
                    monkeys[name] = monkeys[a] * monkeys[b]
                if op == "/":
                    monkeys[name] = monkeys[a] // monkeys[b]

    return monkeys["root"]


def part2(input: str) -> int:
    monkeys = {}
    for line in input.split("\n"):
        name, job = line.split(": ")
        try:
            monkeys[name] = int(job)
        except ValueError:
            monkeys[name] = job.split(" ")

    def resolve(name):
        node = {
            "name": name,
            "left": monkeys[name][0],
            "op": monkeys[name][1],
            "right": monkeys[name][2],
        }

        for branch in ["left", "right"]:
            if node[branch] == "humn":
                node["humn"] = True
            else:
                if type(monkeys[node[branch]]) == int:
                    node[branch] = monkeys[node[branch]]
                else:
                    node[branch] = resolve(node[branch])
                    if "humn" in node[branch]:
                        node["humn"] = True

        return node

    root = resolve("root")

    humn = None

    def evaluate(node):
        left = node["left"]
        if type(left) == dict:
            left = evaluate(left)
        right = node["right"]
        if type(right) == dict:
            right = evaluate(right)

        if left == "humn":
            left = humn
        if right == "humn":
            right = humn

        try:
            if node["op"] == "+":
                return left + right
            elif node["op"] == "-":
                return left - right
            elif node["op"] == "*":
                return left * right
            elif node["op"] == "/":
                return left // right
        except TypeError:
            raise

    node = root

    while node != 'humn':
        for branch in ["left", "right"]:
            if type(node[branch]) == dict and "humn" not in node[branch]:
                node[branch] = evaluate(node[branch])

        if humn is None:
            humn = node["left"] if "humn" not in node["left"] else node["right"]
            node = node["left"] if "humn" in node["left"] else node["right"]
            continue

        value = node["left"] if type(node["left"]) == int else node["right"]

        if node["op"] == "+":
            humn -= value
        elif node["op"] == "-":
            if value == node["left"]:
                humn = value - humn
            else:
                humn += value
        elif node["op"] == "*":
            humn //= value
        elif node["op"] == "/":
            if value == node["left"]:
                humn = value / humn
            else:
                humn *= value

        node = node["left"] if value == node["right"] else node["right"]

    # monkeys["humn"] = humn
    proof = resolve("root")
    proof["humn"] = humn
    left = evaluate(proof["left"])
    right = evaluate(proof["right"])
    assert right == left, f"{left} != {right}"

    return humn


class Test(unittest.TestCase):

    def test_part_1(self):
        self.assertEqual(152, part1(Test.example))

        print(part1(Path('./input.txt').read_text()))

    def test_part_2(self):
        self.assertEqual(301, part2(Test.example))

        print(part2(Path('./input.txt').read_text()))

    example = """
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
""".strip("\n")
