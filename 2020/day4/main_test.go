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
	err := Parse(input, func(p Passport) {
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

var invalidExamples = `eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007`

var validExamples = `pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719`

func TestValidExamples(t *testing.T) {
	validator := NewPassportValidator()
	input := bufio.NewScanner(strings.NewReader(validExamples))

	err := Parse(input, validator.Visitor())

	if err != nil {
		t.Errorf("got error; %v", err)
	}

	validPassports := validator.NumValid()
	if validPassports != 4 {
		t.Errorf("expected %d, got %d", 4, validPassports)
	}
}

func TestInvalidExamples(t *testing.T) {
	validator := NewPassportValidator()
	input := bufio.NewScanner(strings.NewReader(invalidExamples))

	err := Parse(input, validator.Visitor())

	if err != nil {
		t.Errorf("got error; %v", err)
	}

	validPassports := validator.NumValid()
	if validPassports != 0 {
		t.Errorf("expected %d, got %d", 0, validPassports)
	}
}

func TestPart1(t *testing.T) {
	result := Part1()
	if result != 237 {
		t.Errorf("expected %d, got %d", 237, result)
	}
}

func TestValidationRules(t *testing.T) {
	p := Passport{
		Hgt: Height{"170"},
		Pid: "087499704",
		Ecl: "grn",
		Iyr: 2012,
		Eyr: 2030,
		Byr: 1980,
		Hcl: "#623a2f",
	}

	err := (&passportValidator{}).Validate(p)

	if err == nil {
		t.Errorf("wanted an error")
	}
	t.Log(err)

	p.Hgt = Height{"170cm"}

	err = (&passportValidator{}).Validate(p)

	if err != nil {
		t.Errorf("got an error")
	}

	t.Log(err)
}