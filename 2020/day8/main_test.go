package main

import (
	"strings"
	"testing"
)

var exampleInput = `nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6`

func TestExample(t *testing.T) {
	code := strings.Split(exampleInput, "\n")

	result, _ := runProgram(code)

	if result != 5 {
		t.Errorf("got %d want %d", result, 5)
	}
}