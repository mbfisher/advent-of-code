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
	Root   *Node
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

	ruleTrees := make(map[string]*Node)

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
				literalNode := NewNode()
				literalNode.AddEdge(match[1])
				ruleTrees[num] = literalNode
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

			subNodes := make([]*Node, len(subrules))
			for i, subrule := range subrules {
				subNode := NewNode()
				refs := strings.Split(subrule, " ")

				leaves := []*Node{subNode}
				for _, ref := range refs {
					refNode := ruleTrees[ref]

					var nextLeaves []*Node
					for key, child := range refNode.Children {
						for _, leaf := range leaves {
							cloned, _ := child.Clone()
							leaf.AddChild(key, cloned)
							nextLeaves = append(nextLeaves, leaf.Leaves()...)
						}
					}

					leaves = nextLeaves
				}

				subNodes[i] = subNode
			}

			ruleTrees[num] = NewNode()
			MergeNodes(ruleTrees[num], subNodes...)
		}
	}

	return ruleTrees["0"], messages
}
