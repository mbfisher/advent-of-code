package main

import (
	"bufio"
	"strings"
	"testing"
)

func TestExample1(t *testing.T) {
	input := `0: 1 2
1: "a"
2: 1 3 | 3 1
3: "b"`

	Parse(bufio.NewScanner(strings.NewReader(input)))

}