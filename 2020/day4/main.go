package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"
)

type PassportVisitor func(map[string]bool)

func Parse(scanner *bufio.Scanner, visitor PassportVisitor) error {
	var passport map[string]bool

	for scanner.Scan() {
		line := scanner.Text()

		if passport == nil {
			passport = make(map[string]bool)
		}

		if line != "" {
			pairs := strings.Split(line, " ")
			for _, pair := range pairs {
				kv := strings.Split(pair, ":")
				passport[kv[0]] = true
			}
		} else {
			visitor(passport)
			passport = nil
		}

	}

	if err := scanner.Err(); err != nil {
		return err
	}

	// Emit the last passport - we don't get an empty line for it
	visitor(passport)

	return nil
}

var RequiredFields = []string{
	"byr",
	"iyr",
	"eyr",
	"hgt",
	"hcl",
	"ecl",
	"pid",
	"cid",
}

type passportValidator struct {
	numValid int
}

func (v *passportValidator) NumValid() int {
	return v.numValid
}

func (v *passportValidator) Visitor() PassportVisitor {
	return func(passport map[string]bool) {
		var missingFields []string
		for _, field := range RequiredFields {
			if _, ok := passport[field]; !ok {
				missingFields = append(missingFields, field)
			}
		}

		if len(missingFields) == 0 || len(missingFields) == 1 && missingFields[0] == "cid" {
			v.numValid++
		}
	}
}

func NewPassportValidator() *passportValidator {
	return &passportValidator{
		numValid: 0,
	}
}

func Part1() {
	wd, _ := os.Getwd()
	file, err := os.Open(wd + "/day4/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(file)

	validator := NewPassportValidator()

	err = Parse(scanner, validator.Visitor())

	if err != nil {
		log.Fatal(err)
	}

	fmt.Println(validator.NumValid())
}

func Part2() {
}

func main() {
	Part1()
	Part2()
}
