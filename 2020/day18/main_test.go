package main

import "testing"

func TestExamples(t *testing.T) {
	var tests = []struct{
		input string
		result int
	}{
		{"1 + 2 * 3 + 4 * 5 + 6", 71},
		{"1 + (2 * 3) + (4 * (5 + 6))", 51},
		{"2 * 3 + (4 * 5)", 26},
		{"5 + (8 * 3 + 9 + 3 * 4 * 3)", 437},
		{"5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 12240},
		{"((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 13632},
	}

	for _, tt := range tests {
		result := Evaluate(tt.input)
		if result != tt.result {
			t.Fatalf("got %d want %d for %s", result, tt.result, tt.input)
		}
	}
}

func TestAdvanced(t *testing.T) {
	var tests = []struct{
		input string
		result int
	}{
		{"1 + 2 * 3 + 4 * 5 + 6", 231},
		{"1 + (2 * 3) + (4 * (5 + 6))", 51},
		{"2 * 3 + (4 * 5)", 46},
		{"5 + (8 * 3 + 9 + 3 * 4 * 3)", 1445},
		{"5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 669060},
		{"((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 23340},
	}

	for _, tt := range tests {
		result := Advanced(tt.input)
		if result != tt.result {
			t.Fatalf("got %d want %d for %s", result, tt.result, tt.input)
		}
	}
}
