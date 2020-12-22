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
3: "b"
`

	tree, _ := Parse(bufio.NewScanner(strings.NewReader(input)))

	validator := Validator{tree}
	var tests = []struct{
		message string
		result bool
	}{
		{"aab", true},
		{"aba", true},
		{"baa", false},
	}

	for _, tt := range tests {
		if result := validator.Validate(tt.message); result.IsValid != tt.result {
			t.Fatalf("got %t want %t for %s: %s", result.IsValid, tt.result, tt.message, result.Message)
		}
	}
}

func TestExample2(t *testing.T) {
	input := `0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"
`

	tree, _ := Parse(bufio.NewScanner(strings.NewReader(input)))

	validator := Validator{tree}

	var tests = []struct{
		message string
		result bool
	}{
		{"ababbb", true},
		{"bababa", false},
		{"abbbab", true},
		{"aaabbb", false},
		{"aaaabbb", false},
	}

	for _, tt := range tests {
		if result := validator.Validate(tt.message); result.IsValid != tt.result {
			t.Fatalf("got %t want %t for %s: %s", result.IsValid, tt.result, tt.message, result.Message)
		} else {
			t.Logf("got %t for %s", tt.result, tt.message)
		}
	}
}