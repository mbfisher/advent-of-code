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

func TestVersion1(t *testing.T) {
	scanner := bufio.NewScanner(strings.NewReader(exampleInput))
	result := version1(scanner)
	if result != 165 {
		t.Fatalf("got %d want %d", result, 165)
	}
}


var exampleInputV2 = `mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1`

func TestVersion2(t *testing.T) {
	scanner := bufio.NewScanner(strings.NewReader(exampleInputV2))
	result := version2(scanner)
	if result != 208 {
		t.Fatalf("got %d want %d", result, 208)
	}
}
