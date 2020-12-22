package main

import (
	"bufio"
	regexp "regexp"
	strings "strings"
)

var literalRegex = regexp.MustCompile("\"(\\w)\"")

/**
 * e.g.
 *     a
 *    / \
 *   b   c
 *  /     \
 * d       e
 *
 * Root : a
 * Leaves: [d, e]
 */
type RuleTree struct {
	Root *Node
	Leaves []*Node
}

func Parse(scanner *bufio.Scanner) (*Node, []string) {
	rows := make(map[string]string)
	parseRules := true
	var messages []string
	for scanner.Scan() {
		line := scanner.Text()
		if line == "" {
			parseRules = false
			continue
		}

		if parseRules {
			split := strings.Split(line, ":")
			rows[split[0]] = strings.TrimSpace(split[1])
		} else {
			messages = append(messages, line)
		}
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
				// for "a" node looks like:
				// Node{
				//   Children: map[string]Node{
				//     "a": Node{
				//       Children: nil
				//     }
				//   }
				// }
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

			// we make a singe tree
			// when len(subrules) > 1 e.g. "1 3 | 3 1"
			tree := RuleTree{Root: NewNode()}
			for _, subrule := range subrules {
				refs := strings.Split(subrule, " ")
				firstTree, ok := ruleTrees[refs[0]]
				if !ok {
					panic("first tree not OK")
				}

				var firstTreeLeaves []*Node
				for key, child := range firstTree.Root.Children {
					var cloned *Node
					// We don't use firstTree.Leaves here because we need a copy of them
					// Clone() returns the root and leaves
					cloned, nextLeaves := child.Clone()
					tree.Root.AddChild(key, cloned)
					firstTreeLeaves = append(firstTreeLeaves, nextLeaves...)
				}

				secondTree, ok := ruleTrees[refs[1]]
				if !ok {
					panic("second tree not OK")
				}

				var secondTreeLeaves []*Node
				for key, child := range secondTree.Root.Children {
					for _, leaf := range firstTreeLeaves {
						cloned, nextLeaves := child.Clone()
						leaf.AddChild(key, cloned)
						secondTreeLeaves = append(secondTreeLeaves, nextLeaves...)
					}
				}

				tree.Leaves = append(tree.Leaves, secondTreeLeaves...)
			}

			ruleTrees[num] = tree
		}
	}

	return ruleTrees["0"].Root, messages
}