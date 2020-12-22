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

func combat(player1, player2 []int) []int {
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

	if len(player1) == 0 {
		return player2
	} else {
		return player1
	}
}

func getScore(winner []int) int {
	result := 0
	for i := 0; i < len(winner); i++ {
		result += winner[i] * (len(winner) - i)
	}
	return result
}

func recursiveCombat(player1 []int, player2 []int) (int, []int) {
	hands := map[int]map[string]bool{
		1: make(map[string]bool),
		2: make(map[string]bool),
	}

	var winner int

	round := 0
	for len(player1) > 0 && len(player2) > 0 {
		round++
		//fmt.Printf("-- Round %d --\n", round)
		winner = 0

		for i, hand := range map[int][]int{1: player1, 2: player2} {
			key := fmt.Sprintf("%v", hand)
			if hands[i][key] {
				winner = 1
			}
			hands[i][key] = true
		}

		if winner > 0 {
			break
		}

		var a int
		var b int

		//fmt.Printf("%v\n", player1)
		//fmt.Printf("%v\n", player2)

		// Draw a card from each players hand
		a, player1 = player1[0], player1[1:]
		b, player2 = player2[0], player2[1:]

		// If both players have at least as many cards remaining in their deck as the value of the card
		// they just drew, the winner of the round is determined by playing a new game of Recursive Combat
		if len(player1) >= a && len(player2) >= b {
			player1Sub := make([]int, a)
			copy(player1Sub, player1[:a])
			player2Sub := make([]int, b)
			copy(player2Sub, player2[:b])
			winner, _ = recursiveCombat(player1Sub, player2Sub)
		} else {
			// Otherwise, at least one hand must not have enough cards left in their deck to recurse;
			// the winner of the round is the hand with the higher-value card.
			if a > b {
				winner = 1
			} else {
				winner = 2
			}
		}

		//fmt.Printf("Round winner: %d\n", winner)
		if winner == 1 {
			player1 = append(player1, a, b)
		} else {
			player2 = append(player2, b, a)
		}
	}

	//fmt.Printf("Game winner: %d\n", winner)
	if winner == 1 {
		return 1, player1
	} else {
		return 2, player2
	}
}

func Part1() int {
	wd, _ := os.Getwd()
	file, err := os.Open(wd + "/day22/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(file)
	player1, player2 := parse(scanner)
	winner := combat(player1, player2)
	result := getScore(winner)

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
	player1, player2 := parse(scanner)
	_, winner := recursiveCombat(player1, player2)
	result := getScore(winner)

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return result
}

func main() {
	//fmt.Println(Part1())
	fmt.Println(Part2())
}
