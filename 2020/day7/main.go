package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"regexp"
	"strconv"
	"strings"
)

type BagMap map[string]Bag

type Bag struct {
	Color    string
	Count    int
	Contains BagMap
}

var bagPattern = regexp.MustCompile("^([a-z\\s]+)bags contain")
var containsPattern = regexp.MustCompile("(\\d+) ([a-z ]+)bag")

func parseInput(scanner *bufio.Scanner) BagMap {
	bags := make(map[string]Bag)

	newBag := func(color string) Bag {
		if bag, ok := bags[color]; ok {
			return bag
		}

		bag := Bag{
			Color:    color,
			Count:    1,
			Contains: make(map[string]Bag),
		}
		bags[color] = bag
		return bag
	}

	for scanner.Scan() {
		line := scanner.Text()

		outer := bagPattern.FindStringSubmatch(line)
		contains := containsPattern.FindAllStringSubmatch(line, -1)

		color := strings.TrimSpace(outer[1])

		bag := newBag(color)

		for _, inner := range contains {
			color := strings.TrimSpace(inner[2])
			innerBag := newBag(color)
			count, _ := strconv.Atoi(inner[1])
			// innerBag.Count is a copy of bags[color].Count, so updating it here is immutable
			// innerBag.Contains is a reference to bags[color].Contains - we don't need to copy it
			innerBag.Count = count
			bag.Contains[color] = innerBag
		}
	}

	return bags
}

func checkBag(bag Bag, bags BagMap, result *map[string]bool) bool {
	if check, ok := (*result)[bag.Color]; ok {
		return check
	}

	_, ok := bag.Contains["shiny gold"]

	if ok {
		(*result)[bag.Color] = ok
		return true
	}

	for innerColor, _ := range bag.Contains {
		innerBag := bags[innerColor]
		check := checkBag(innerBag, bags, result)
		(*result)[innerColor] = check
		if check {
			return true
		}
	}

	return false
}

func findShinyGold(bags BagMap) int {
	result := make(map[string]bool)
	for color, bag := range bags {
		if color == "shiny gold" {
			continue
		}

		result[color] = checkBag(bag, bags, &result)
	}

	numBags := 0
	for _, match := range result {
		if match {
			numBags++
		}
	}

	return numBags
}

func sumBags (bag Bag) int {
	if bag.Contains == nil {
		return 1
	}

	result := 1
	for _, innerBag := range bag.Contains {
		innerSum := sumBags(innerBag)
		result += innerSum * innerBag.Count
	}
	return result
}

func sumShinyGold(bags BagMap) int {
	return sumBags(bags["shiny gold"]) - 1
}

func Part1() {
	wd, _ := os.Getwd()
	file, err := os.Open(wd + "/day7/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(file)

	bags := parseInput(scanner)

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	fmt.Println(findShinyGold(bags))
}

func Part2() {
	wd, _ := os.Getwd()
	file, err := os.Open(wd + "/day7/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(file)

	bags := parseInput(scanner)

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	fmt.Println(sumShinyGold(bags))
}

func main() {
	//Part1()
	Part2()
}
