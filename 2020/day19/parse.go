package main

import (
	"bufio"
	regexp "regexp"
	strings "strings"
)

var literalRegex = regexp.MustCompile("\"(\\w)\"")

type RuleTree struct {
	Root *Node
	Leaves []*Node
}

func Parse(scanner *bufio.Scanner) error {
	rows := make(map[string]string)
	for scanner.Scan() {
		line := scanner.Text()
		split := strings.Split(line, ":")
		rows[split[0]] = strings.TrimSpace(split[1])
	}

	ruleTrees := make(map[string]RuleTree)

	// keep looping whilst we've not built all the rows into nodes
	for len(ruleTrees) != len(rows) {
		// for each row
		for num, rule := range rows {
			// check if we've already built the node and break
			if _, ok := ruleTrees[num]; ok {
				continue
			}

			// is the rule a literal?
			if match := literalRegex.FindStringSubmatch(rule); match != nil {
				root := NewNode()
				ruleTrees[num] = RuleTree{
					Root: root,
					Leaves: []*Node{root.AddEdge(match[1])},
				}
				continue
			}

			// parse sub-ruleTrees

			subrules := strings.Split(rule, " | ")
			references := make([]string, 0, 4)

			for _, subrule := range subrules {
				references = append(references, strings.Split(subrule, " ")...)
			}


			canProcess := true
			for _, ref := range references {
				if _, ok := ruleTrees[ref]; !ok {
					// we have a row depending on a rule we haven't processed yet
					canProcess = false
					break
				}
			}

			if !canProcess {
				continue
			}

			tree := RuleTree{Root: NewNode()}
			for _, subrule := range subrules {
				refs := strings.Split(subrule, " ")
				firstTree, ok := ruleTrees[refs[0]]
				if !ok {
					panic("first tree not OK")
				}

				// tree.Root = firstTree.Root
				var tempLeaves []*Node
				for key, child := range firstTree.Root.Children {
					var cloned *Node
					cloned, tempLeaves = child.Clone()
					tree.Root.AddChild(key, cloned)
				}
				//if i == 0 {
				//} else {
				//	tree.Root.
				//}

				secondTree, ok := ruleTrees[refs[1]]
				if !ok {
					panic("second tree not OK")
				}
				var finalLeaves []*Node
				for key, value := range secondTree.Root.Children {
					for _, leaf := range tempLeaves {
						cloned, nextLeaves := value.Clone()
						leaf.AddChild(key, cloned)
						finalLeaves = append(finalLeaves, nextLeaves...)
					}
				}

				tree.Leaves = append(tree.Leaves, finalLeaves...)
			}
			ruleTrees[num] = tree


		}
	}

	return nil
}