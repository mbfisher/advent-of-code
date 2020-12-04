package main

import (
	"bufio"
	"strings"
	"testing"
)

var exampleInput = `ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in`

func TestParse(t *testing.T) {
	numPassports := 0
	input := bufio.NewScanner(strings.NewReader(exampleInput))
	err := Parse(input, func(p map[string]bool) {
		numPassports++
	})

	if err != nil {
		t.Errorf("got error; %v", err)
	}

	if numPassports != 4 {
		t.Errorf("expected %d, got %d", 4, numPassports)
	}
}

func TestPassportValidator(t *testing.T) {
	validator := NewPassportValidator()
	input := bufio.NewScanner(strings.NewReader(exampleInput))

	err := Parse(input, validator.Visitor())

	if err != nil {
		t.Errorf("got error; %v", err)
	}

	validPassports := validator.NumValid()
	if validPassports != 2 {
		t.Errorf("expected %d, got %d", 2, validPassports)
	}
}
