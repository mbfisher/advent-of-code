package main

import (
	"bufio"
	"fmt"
	"strings"
	"testing"
)


func TestExample1(t *testing.T) {
	input := `0: 1 2
1: "a"
2: 1 3 | 3 1
3: "b"
`

	tree, _ := Parse(bufio.NewScanner(strings.NewReader(input)))
	validator := Validator{tree}

	var tests = []struct{
		message string
		result bool
	}{
		{"aab", true},
		{"aba", true},
		{"baa", false},
	}

	for _, tt := range tests {
		if result := validator.Validate(tt.message); result.IsValid != tt.result {
			t.Fatalf("got %t want %t for %s: %s", result.IsValid, tt.result, tt.message, result.Message)
		}
	}
}

func TestExample2(t *testing.T) {
	input := `0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"
`
	tree, _ := Parse(bufio.NewScanner(strings.NewReader(input)))

	validator := Validator{tree}

	var tests = []struct{
		message string
		result bool
	}{
		{"ababbb", true},
		{"bababa", false},
		{"abbbab", true},
		{"aaabbb", false},
		{"aaaabbb", false},
		{"aaa", false},
	}

	for _, tt := range tests {
		if result := validator.Validate(tt.message); result.IsValid != tt.result {
			t.Fatalf("got %t want %t for %s: %s", result.IsValid, tt.result, tt.message, result.Message)
		}
	}
}

func TestExample3(t *testing.T) {
	input := `0: 1 4
1: "a"
2: 1 3 | 3 1
3: "b"
4: 2 1 | 3 3`

	tree, _ := Parse(bufio.NewScanner(strings.NewReader(input)))

	validator := Validator{tree}

	var tests = []struct{
		message string
		result bool
	}{
		{"aaba", true},
		{"abaa", true},
		{"abb", true},
	}

	for _, tt := range tests {
		if result := validator.Validate(tt.message); result.IsValid != tt.result {
			t.Fatalf("got %t want %t for %s: %s", result.IsValid, tt.result, tt.message, result.Message)
		} else {
			t.Logf("got %t for %s", tt.result, tt.message)
		}
	}
}


func TestPart2Example1(t *testing.T) {
	input := `42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31 | 42 11 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42 | 42 8
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba`

	tree, messages := Parse(bufio.NewScanner(strings.NewReader(input)))

	validator := Validator{tree}

	result := 0
	for _, message := range messages {
		if validationResult := validator.Validate(message); validationResult.IsValid {
			result++
			fmt.Printf("%s: ✅\n", message)
		} else {
			fmt.Printf("%s: %s\n", message, validationResult.Message)
		}
	}

	if result != 3 {
		t.Fatalf("got %d want 3", result)
	}

	//var tests = []struct{
	//	message string
	//	result bool
	//}{
	//	{"bbabbbbaabaabba", true},
	//	{"ababaaaaaabaaab", true},
	//	{"ababaaaaabbbaba", true},
	//}
	//
	//for _, tt := range tests {
	//	if result := validator.Validate(tt.message); result.IsValid != tt.result {
	//		t.Fatalf("got %t want %t for %s: %s", result.IsValid, tt.result, tt.message, result.Message)
	//	} else {
	//		t.Logf("got %t for %s", tt.result, tt.message)
	//	}
	//}
}