package main

import (
	"bufio"
	"strings"
	"testing"
)

func TestPart1(t *testing.T) {
	input := `Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10`

	player1, player2 := parse(bufio.NewScanner(strings.NewReader(input)))
	result := combat(player1, player2)
	if result != 306 {
		t.Fatalf("got %d want 306", result)
	}
}