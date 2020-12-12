package main

import (
	"bufio"
	"strings"
	"testing"
)

var exampleInput = `F10
N3
F7
R90
F11`

func TestGetManhattanDistance(t *testing.T) {
	scanner := bufio.NewScanner(strings.NewReader(exampleInput))
	result := getManhattanDistance(scanner)
	if result != 25 {
		t.Fatalf("got %d want %d", result, 25)
	}
}

func TestFollowWaypoint(t *testing.T) {
	scanner := bufio.NewScanner(strings.NewReader(exampleInput))
	result := followWaypoint(scanner)
	if result != 286 {
		t.Fatalf("got %d want %d", result, 286)
	}
}