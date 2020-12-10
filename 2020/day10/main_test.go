package main

import (
	"bufio"
	"strings"
	"testing"
)

var exampleInput = `16
10
15
5
1
11
7
19
6
12
4`

func TestFindJoltDifferenceProduct(t *testing.T) {
	scanner := bufio.NewScanner(strings.NewReader(exampleInput))
	result := findJoltDifferenceProduct(scanner)

	if result != 35 {
		t.Errorf("got %d want %d", result, 35)
	}
}

var exampleInput2 = `28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3`

func TestFindCombinations(t *testing.T) {
	scanner := bufio.NewScanner(strings.NewReader(exampleInput))
	result := findCombinations(scanner)

	if result != 8 {
		t.Errorf("got %d want %d", result, 8)
	}
}

func TestFindCombinations2(t *testing.T) {
	scanner := bufio.NewScanner(strings.NewReader(exampleInput2))
	result := findCombinations(scanner)

	if result != 19208 {
		t.Errorf("got %d want %d", result, 19208)
	}
}