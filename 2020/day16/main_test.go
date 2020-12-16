package main

import (
	"bufio"
	"strings"
	"testing"
)

var exampleInput = `class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12`

func TestParse(t *testing.T) {
	scanner := bufio.NewScanner(strings.NewReader(exampleInput))
	input := parse(scanner)

	if len(input.Fields) != 3 {
		t.Fatalf("got %d fields, want 3", len(input.Fields))
	}

	if len(input.MyTicket) != 3 {
		t.Fatalf("got %d for MyTicket, want 3", len(input.MyTicket))
	}

	if len(input.NearbyTickets) != 4 {
		t.Fatalf("got %d nearby tickets, want 4", len(input.NearbyTickets))
	}
}

func TestGetTicketScanningErrorRate(t *testing.T) {
	scanner := bufio.NewScanner(strings.NewReader(exampleInput))
	result := getTicketScanningErrorRate(parse(scanner))

	if result != 71 {
		t.Fatalf("got %d, want 71", result)
	}
}

func TestGetFieldPositions(t *testing.T) {
	result := getFieldPositions(parse(bufio.NewScanner(strings.NewReader(`class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9`))))

	if result["row"] != 0 {
		t.Fatalf("got %d for row position, want 1", result["row"])
	}

	if result["class"] != 1 {
		t.Fatalf("got %d for class position, want 1", result["class"])
	}

	if result["seat"] != 2 {
		t.Fatalf("got %d for seat position, want 2", result["seat"])
	}
}