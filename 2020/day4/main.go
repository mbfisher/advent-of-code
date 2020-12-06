package main

import (
	"bufio"
	"fmt"
	"github.com/go-playground/validator/v10"
	"log"
	"os"
	"reflect"
	"strconv"
	"strings"
)

type Height struct {
	value string
}

type Passport struct {
	Byr int    `validate:"required,gte=1920,lte=2002"`
	Iyr int    `validate:"required,gte=2010,lte=2020"`
	Eyr int    `validate:"required,gte=2020,lte=2030"`
	Hgt Height `validate:"required"`
	Hcl string `validate:"required,hexcolor"`
	Ecl string `validate:"required,oneof=amb blu brn gry grn hzl oth"`
	Pid string `validate:"required,len=9,containsany=0123456789"`
	Cid string
}

type PassportVisitor func(Passport)

func Parse(scanner *bufio.Scanner, visitor PassportVisitor) error {
	var fields map[string]string

	visit := func() {
		byr, _ := strconv.Atoi(fields["byr"])
		iyr, _ := strconv.Atoi(fields["iyr"])
		eyr, _ := strconv.Atoi(fields["eyr"])
		passport := Passport{
			Byr: byr,
			Iyr: iyr,
			Eyr: eyr,
			Hgt: Height{fields["hgt"]},
			Hcl: fields["hcl"],
			Ecl: fields["ecl"],
			Pid: fields["pid"],
			Cid: fields["cid"],
		}
		visitor(passport)
	}

	for scanner.Scan() {
		line := scanner.Text()

		if fields == nil {
			fields = make(map[string]string)
		}

		if line != "" {
			pairs := strings.Split(line, " ")
			for _, pair := range pairs {
				kv := strings.Split(pair, ":")
				fields[kv[0]] = kv[1]
			}
		} else {
			visit()
			fields = nil
		}
	}

	if err := scanner.Err(); err != nil {
		return err
	}

	// Emit the last passport - we don't get an empty line for it
	visit()

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

func ValidateHeight(field reflect.Value) interface{} {
	if value, ok := field.Interface().(string); ok {
		fmt.Println(value)
	}

	return nil
}

type passportValidator struct {
	numValid int
}

func (v *passportValidator) NumValid() int {
	return v.numValid
}

func (v *passportValidator) validateHeight(field reflect.Value) interface{} {
	if hgt, ok := field.Interface().(Height); ok {
		if len(hgt.value) < 4 {
			return nil
		}

		value, _ := strconv.Atoi(hgt.value[:len(hgt.value)-2])
		unit := hgt.value[len(hgt.value)-2:]

		if unit == "cm" && value >= 150 && value <= 193 {
			return hgt.value
		}

		if unit == "in" && value >= 59 && value <= 76 {
			return hgt.value
		}

		return nil
	}

	return nil
}

func (v *passportValidator) Validate(passport Passport) error {
	validate := validator.New()
	validate.RegisterCustomTypeFunc(v.validateHeight, Height{})
	return validate.Struct(&passport)
}

func (v *passportValidator) Visitor() PassportVisitor {
	return func(passport Passport) {
		//var missingFields []string
		//isValid := true
		//
		//if val, ok := passport["byr"]; ok {
		//	byr, err := strconv.Atoi(val)
		//	if err != nil {
		//		fmt.Printf("byr: '%s' is not a number\n", val)
		//	} else if byr < 1920 || byr > 2002 {
		//		fmt.Printf("byr: '%d' out of range\n", byr)
		//	} else {
		//		isValid = true
		//	}
		//} else {
		//	missingFields = append(missingFields, "byr")
		//}
		//
		//if isValid {
		//	v.numValid++
		//}

		err := v.Validate(passport)

		if err == nil {
			v.numValid++
		} else {
			validationErrors := err.(validator.ValidationErrors)
			fmt.Println(passport)
			fmt.Println(validationErrors)
		}

		//if len(missingFields) == 0 || len(missingFields) == 1 && missingFields[0] == "cid" {
		//	v.numValid++
		//}
	}
}

func NewPassportValidator() *passportValidator {
	return &passportValidator{
		numValid: 0,
	}
}

func Part1() int {
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

	return validator.NumValid()
}

func Part2() {
}

func main() {
	fmt.Println(Part1())
	Part2()
}
