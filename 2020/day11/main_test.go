package main

import (
	"bufio"
	"strings"
	"testing"
)

var exampleInput = `L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL`

var afterFirstRound = `#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##
`

var afterSecondRound = `#.LL.L#.##
#LLLLLL.L#
L.L.L..L..
#LLL.LL.L#
#.LL.LL.LL
#.LLLL#.##
..L.L.....
#LLLLLLLL#
#.LLLLLL.L
#.#LLLL.##
`

var afterThirdRound = `#.##.L#.##
#L###LL.L#
L.#.#..#..
#L##.##.L#
#.##.LL.LL
#.###L#.##
..#.#.....
#L######L#
#.LL###L.L
#.#L###.##
`

var afterFourthRound = `#.#L.L#.##
#LLL#LL.L#
L.L.L..#..
#LLL.##.L#
#.LL.LL.LL
#.LL#L#.##
..L.L.....
#L#LLLL#L#
#.LLLLLL.L
#.#L#L#.##
`

var afterFifthRound = `#.#L.L#.##
#LLL#LL.L#
L.#.L..#..
#L##.##.L#
#.#L.LL.LL
#.#L#L#.##
..L.L.....
#L#L##L#L#
#.LLLLLL.L
#.#L#L#.##
`

func TestDoRound(t *testing.T) {
	scanner := bufio.NewScanner(strings.NewReader(exampleInput))
	seats := parse(scanner)

	tests := []struct{
		result string
	}{
		{afterFirstRound},
		{afterSecondRound},
		{afterThirdRound},
		{afterFourthRound},
		{afterFifthRound},
	}

	for i, tt := range tests {
		seats = doRound(seats)
		result := stringify(seats)
		if result != tt.result {
			t.Errorf("round %d failed", i + 1)
			t.Log(result)
		}
	}
}

func TestCountOccupied(t *testing.T) {
	scanner := bufio.NewScanner(strings.NewReader(exampleInput))
	result := countOccupied(scanner)
	if result != 37 {
		t.Errorf("got %d want %d", result, 37)
	}
}