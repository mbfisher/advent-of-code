package main

import (
	"bufio"
	"strings"
	"testing"
)

var exampleInput = `mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0`

func TestSumValues(t *testing.T) {
	scanner := bufio.NewScanner(strings.NewReader(exampleInput))
	result := sumValues(scanner)
	if result != 165 {
		t.Fatalf("got %d want %d", result, 25)
	}
}
