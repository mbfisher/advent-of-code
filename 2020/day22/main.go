package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
)

func parse(scanner *bufio.Scanner) ([]int, []int) {
	players := make([][]int, 2)

	scanner.Scan()

	i := 0
	for scanner.Scan() {
		line := scanner.Text()

		if line == "" {
			continue
		}

		if line == "Player 2:" {
			i = 1
			continue
		}

		value, _ := strconv.Atoi(line)
		players[i] = append(players[i], value)
	}

	return players[0], players[1]
}

func combat(player1, player2 []int) int {
	for len(player1) > 0 && len(player2) > 0 {
		var a int
		var b int
		a, player1 = player1[0], player1[1:]
		b, player2 = player2[0], player2[1:]

		if a > b {
			player1 = append(player1, a, b)
		} else {
			player2 = append(player2, b, a)
		}
	}

	var winner []int
	if len(player1) == 0 {
		winner = player2
	} else {
		winner = player1
	}

	result := 0
	for i := 0; i < len(winner); i++ {
		result += winner[i] * (len(winner) - i)
	}
	return result
}

func Part1() int {
	wd, _ := os.Getwd()
	file, err := os.Open(wd + "/day22/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(file)
	player1, player2 := parse(scanner)
	result := combat(player1, player2)

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return result
}

func Part2() int {
	wd, _ := os.Getwd()
	file, err := os.Open(wd + "/day22/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(file)
	result := 0

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return result
}

func main() {
	fmt.Println(Part1())
	//fmt.Println(Part2())
}
