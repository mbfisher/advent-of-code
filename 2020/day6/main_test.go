package main

import "testing"

func TestCountGroupAnyone(t *testing.T) {
	var tests = []struct{
		group []string
		want int
	}{
		{[]string{"abc"}, 3},
		{[]string{"a", "b", "c"}, 3},
		{[]string{"ab", "ac"}, 3},
		{[]string{"a", "a", "a", "a"}, 1},
		{[]string{"b"}, 1},
	}

	for _, tt := range tests {
		got := countGroupAnyone(tt.group)
		if got != tt.want {
			t.Errorf("got %d want %d", got, tt.want)
		}
	}
}

func TestCountGroupEveryone(t *testing.T) {
	var tests = []struct{
		group []string
		want int
	}{
		{[]string{"abc"}, 3},
		{[]string{"a", "b", "c"}, 0},
		{[]string{"ab", "ac"}, 1},
		{[]string{"a", "a", "a", "a"}, 1},
		{[]string{"b"}, 1},
	}

	for _, tt := range tests {
		got := countGroupEveryone(tt.group)
		if got != tt.want {
			t.Errorf("got %d want %d", got, tt.want)
		}
	}
}