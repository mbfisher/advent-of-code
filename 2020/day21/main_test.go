package main

import (
	"bufio"
	"fmt"
	"strings"
	"testing"
)

var input = `mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)`

func TestParse(t *testing.T) {
	recipes, ingredients, allergens := parse(bufio.NewScanner(strings.NewReader(input)))
	fmt.Println(recipes)
	fmt.Println(allergens)
	fmt.Println(ingredients)
}

func TestNoAllergens(t *testing.T) {
	_, ingredients, allergens := parse(bufio.NewScanner(strings.NewReader(input)))
	result := noAllergens(allergens, ingredients)
	want := set([]string{"mxmxvkd", "kfcds", "sqjhc", "nhms"})
	if result.Equals(want) {
		t.Fatalf("got %v want %v", result, want)
	}
}

func TestPart1(t *testing.T) {
	result := part1(bufio.NewScanner(strings.NewReader(input)))
	if result != 5 {
		t.Fatalf("got %d want 5", result)
	}
}

func TestPart2(t *testing.T) {
	result := part2(bufio.NewScanner(strings.NewReader(input)))
	if result != "mxmxvkd,sqjhc,fvjkl" {
		t.Fatalf("got %s want mxmxvkd,sqjhc,fvjkl", result)
	}
}