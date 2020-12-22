package main

type Node struct {
	Children map[string]*Node
	Recurse  *Node
}

func NewNode() *Node {
	return &Node{Children: make(map[string]*Node)}
}

func (n *Node) Clone() (root *Node, leaves []*Node) {
	return n.cloneFromRoot(make(map[*Node]*Node))
}

func (n *Node) cloneFromRoot(cloned map[*Node]*Node) (node *Node, leaves []*Node) {
	node = NewNode()
	cloned[n] = node

	if n.Recurse != nil {
		if cl, ok := cloned[n.Recurse]; ok {
			node.Recurse = cl
		} else {
			node.Recurse = n.Recurse
		}
	}

	for k, v := range n.Children {
		child, cl := v.cloneFromRoot(cloned)
		node.Children[k] = child
		leaves = append(leaves, cl...)
	}

	if len(node.Children) == 0 {
		leaves = []*Node{node}
	}

	return node, leaves
}

func (n *Node) AddEdge(value string) *Node {
	return n.AddChild(value, NewNode())
}

func MergeNodes(dest *Node, srcs ...*Node) {
	for _, src := range srcs {
		if src.Recurse != nil {
			if dest.Recurse != nil {
				panic("cant overwrite Recurse")
			}

			dest.Recurse = src.Recurse
		}

		for key, child := range src.Children {
			if existing, ok := dest.Children[key]; ok {
				MergeNodes(existing, child)
			} else {
				dest.Children[key] = child
			}
		}
	}
}

func (n *Node) AddChild(value string, node *Node) *Node {
	n.Children[value] = node
	return node
}

func (n *Node) Leaves() (result []*Node) {
	for _, child := range n.Children {
		if len(child.Children) == 0 { // && child.Recurse == nil {
			result = append(result, child)
		} else {
			result = append(result, child.Leaves()...)
		}
	}

	return
}
