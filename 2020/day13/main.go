package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"math"
	"os"
	"strconv"
	"strings"
)

func getFirstDepartureAfterTimestamp(timestamp int64, bus int) int64 {
	d := math.Ceil(float64(timestamp) / float64(bus))
	return int64(float64(bus) * d)
}

func findEarliestBus(input string) int {
	lines := strings.Split(input, "\n")
	ts, _ := strconv.Atoi(lines[0])
	timestamp := int64(ts)

	var buses []int
	for _, id := range strings.Split(lines[1], ",") {
		if id == "x" {
			continue
		}
		num, _ := strconv.Atoi(id)
		buses = append(buses, num)
	}

	min := timestamp * 2
	var bus int
	for _, id := range buses {
		next := getFirstDepartureAfterTimestamp(timestamp, id)
		if next < min {
			min = next
			bus = id
		}
	}

	return bus * int(min - timestamp)
}

func findWeirdTimestamp(input string, start int64) int64 {
	lines := strings.Split(input, "\n")

	buses := make(map[int]int)
	for i, id := range strings.Split(lines[1], ",") {
		if id == "x" {
			continue
		}
		num, _ := strconv.Atoi(id)
		buses[i] = num
	}

	i := start
	var ts int64
	for true {
		ts = int64(buses[0]) * i
		good := true

		for pos, id := range buses {
			if pos == 0 {
				continue
			}

			next := getFirstDepartureAfterTimestamp(ts, id)

			if next - ts != int64(pos) {
				good = false
				break
			}
		}

		if good {
			break
		}

		i++
	}

	fmt.Println(i)
	return ts
}

func Part1() int {
	wd, _ := os.Getwd()
	dat, err := ioutil.ReadFile(wd + "/day13/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	input := string(dat)
	return findEarliestBus(input)
}

func Part2() int64 {
	wd, _ := os.Getwd()
	dat, err := ioutil.ReadFile(wd + "/day13/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	input := string(dat)
	return findWeirdTimestamp(input, 100000000000000)
}

func main() {
	//fmt.Println(Part1())
	fmt.Println(Part2())
}
