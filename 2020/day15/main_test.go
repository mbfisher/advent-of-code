package main

import (
	"testing"
)

func TestNumber2020(t *testing.T) {
	var tests = []struct {
		input  string
		result int
	}{
		{"0,3,6", 436},
		{"1,3,2", 1},
		{"2,1,3", 10},
		{"1,2,3", 27},
		{"2,3,1", 78},
		{"3,2,1", 438},
		{"3,1,2", 1836},
	}

	for _, tt := range tests {
		result := nthSpoken(tt.input, 2020)
		if result != tt.result {
			t.Fatalf("got %d want %d", result, tt.result)
		}
	}
}

func TestNumber30000000(t *testing.T) {
	var tests = []struct {
		input  string
		result int
	}{
		{"0,3,6", 175594},
		//{"1,3,2", 2578},
		//{"2,1,3", 3544142},
		//{"1,2,3", 261214},
		//{"2,3,1", 6895259},
		//{"3,2,1", 18},
		//{"3,1,2", 362},
	}

	for _, tt := range tests {
		result := nthSpoken(tt.input, 30000000)
		if result != tt.result {
			t.Fatalf("got %d want %d", result, tt.result)
		}
	}
}