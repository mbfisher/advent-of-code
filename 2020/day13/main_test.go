package main

import "testing"

var exampleInput = `939
7,13,x,x,59,x,31,19`

func TestFindEarliestBus(t *testing.T) {
	result := findEarliestBus(exampleInput)
	if result != 295 {
		t.Fatalf("got %d want %d", result, 295)
	}
}

func TestFindWeirdTimestamp(t *testing.T) {
	var tests = []struct{
		input string
		result int64
	}{
		{"\n7,13,x,x,59,x,31,19", 1068781},
		{"\n67,7,59,61", 754018},
		{"\n67,x,7,59,61", 779210},
		{"\n67,7,x,59,61", 1261476},
		{"\n1789,37,47,1889", 1202161486},
	}

	for _, tt := range tests {
		result := findWeirdTimestamp(tt.input, 1)
		if result != tt.result {
			t.Fatalf("got %d want %d", result, tt.result)
		}
	}
}