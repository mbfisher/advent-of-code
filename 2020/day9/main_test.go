package main

import (
	"bufio"
	"strings"
	"testing"
)

var exampleInput = `35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576`

func TestFindFirstBad(t *testing.T) {
	scanner := bufio.NewScanner(strings.NewReader(exampleInput))
	result := findFirstBad(scanner, 5)

	if result != 127 {
		t.Errorf("got %d want %d", result, 127)
	}
}

func TestFindWeakness(t *testing.T) {
	scanner := bufio.NewScanner(strings.NewReader(exampleInput))
	result := findWeakness(scanner, 127)

	if result != 62 {
		t.Errorf("got %d want %d", result, 62)
	}
}