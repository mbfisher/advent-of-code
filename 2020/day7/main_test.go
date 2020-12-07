package main

import (
	"bufio"
	"strings"
	"testing"
)

var exampleInput = `light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.`

func TestFindShinyGold(t *testing.T) {
	input := bufio.NewScanner(strings.NewReader(exampleInput))
	bags := parseInput(input)
	result := findShinyGold(bags)

	if result != 4 {
		t.Errorf("got %d want %d", result, 4)
	}
}

func TestSumShinyGold(t *testing.T) {
	input := bufio.NewScanner(strings.NewReader(exampleInput))
	bags := parseInput(input)
	result := sumShinyGold(bags)

	if result != 32 {
		t.Errorf("got %d want %d", result, 32)
	}
}