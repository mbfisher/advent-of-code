package main

import "testing"

func TestGetRow(t *testing.T) {
	var tests = []struct {
		spec string
		want int
	}{
		{"FBFBBFF", 44},
		{"BFFFBBF", 70},
		{"FFFBBBF", 14},
		{"BBFFBBF", 102},
		{"BBFFBBB", 103},
	}

	for _, tt := range tests {
		got := getRow(tt.spec)
		if got != tt.want {
			t.Errorf("got %d want %d", got, tt.want)
		}
	}
}

func TestGetCol(t *testing.T) {
	var tests = []struct {
		spec string
		want int
	}{
		{"RLR", 5},
		{"RRR", 7},
		{"RLL", 4},
	}

	for _, tt := range tests {
		got := getCol(tt.spec)
		if got != tt.want {
			t.Errorf("got %d want %d", got, tt.want)
		}
	}
}

func TestGetSeatID(t *testing.T) {
	var tests = []struct {
		spec string
		want int
	}{
		{"BFFFBBFRRR", 567},
		{"FFFBBBFRRR", 119},
		{"BBFFBBFRLL", 820},
	}

	for _, tt := range tests {
		got := getSeatID(tt.spec)
		if got != tt.want {
			t.Errorf("got %d want %d", got, tt.want)
		}
	}
}