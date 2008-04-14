def list_and(atoms, conditions):
    final = 1

    for ato in atoms:
        for cond in conditions:
            final = cond(ato)
            if not final:
                break
        if not final:
            break

    return final

def list_or(atoms, conditions):
    final = 0

    for ato in atoms:
        for cond in conditions:
            final = cond(ato)
            if final:
                break
        if final:
            break

    return final

letter_conditions = [lambda x: x != '\n',
                     lambda x: x != '\t',
                     lambda x: x != '\ ',
                     lambda x: x >= 'a' and x <='z']

def fac(n, a):
    if n == 1:
        return a
    else:
        return fac(n - 1, a * n)



class graph_node:

    def __init__(self, tag, value):
        self.tag = tag
        self.value = value
        self.edges = {}

    def __repr__(self):
        rep = self.tag + " " + str(self.value) + ": "
        edgekeys = self.edges.keys()
        edgekeys.sort()
        for edgekey in edgekeys:
            edge = self.edges[edgekey]
            rep += edge.other(self.tag).tag + "-" + str(edge.value) + " "
        return rep
        
    def add_edge(self, edge):
        other = edge.other(self.tag)
        self.edges[other.tag] = edge

    def find_edge(self, other):
        if self.edges.has_key(other.tag):
            return self.edges[other.tag]
        else:
            edge = graph_edge(self, other, 0)
            self.add_edge(edge)
            other.add_edge(edge)

            return edge

    def neighbor_tags(self):
        tags = []
        for edge in self.edges:
            tags.append(edge.other(self.tag).tag)
        return tags

class graph_edge:

    def __init__(self, a, b, value):
        self.nodes = (a, b)
        self.value = value

    def contains_node(self, tag):
        return tag == self.nodes[0].tag or tag == self.nodes[1].tag

    def other(self, tag):
        if tag == self.nodes[0].tag:
            return self.nodes[1]
        else:
            return self.nodes[0]

class graph:

    def __init__(self):
        self.nodes = {}

    def __repr__(self):
        rep = ""
        nodekeys = self.nodes.keys()
        nodekeys.sort()
        for nodekey in nodekeys:
            node = self.nodes[nodekey]
            rep += str(node) + "\n"
        return rep

    def add_node(self, node):
        self.nodes[node.tag] = node

    def find_node(self, tag):
        if self.nodes.has_key(tag):
            return self.nodes[tag]
        else:
            node = graph_node(tag, 1)
            self.nodes[tag] = node
            return node

    def contains_node(self, tag):
        if self.nodes.has_key(tag):
            return 1
        else:
            return 0

    def connect(self, pair):
        anode = self.find_node(pair[0])
        bnode = self.find_node(pair[1])

        edge = anode.find_edge(bnode)

        anode.add_edge(edge)
        bnode.add_edge(edge)

        return edge

    def find_edge(self, pair):
        anode = self.find_node(pair[0])
        bnode = self.find_node(pair[1])
        return anode.find_edge(bnode)


class letter_graph(graph):
    def __init__(self):
        graph.__init__(self)
        
    def letter_pair(self, pair):
        self.find_node(pair[0]).value += 1
        self.find_node(pair[1]).value += 1
        self.find_edge(pair).value += 1
        


def graph_pairs(file):
    text = open(file).read()
    graph = letter_graph()
    index = 0

    while index < len(text) - 1:
        a = text[index].lower()
        b = text[index + 1].lower()

        if(list_and([a, b], letter_conditions)):
            graph.letter_pair((a, b))

        index += 1

    return graph
    















def count_pairs(file):
    text = open(file).read()
    pairs = {}
    index = 0;
    
    while index < len(text) - 1:
        a = text[index]
        b = text[index + 1]

        if list_and([a, b], letter_conditions) and a != b:
            pair = '' + a.lower() + b.lower()

            if not pairs.has_key(pair):
                pairs[pair] = 0

            pairs[pair] += 1

        index += 1

    return pairs

def swap(ls, a, b):
    c = ls[a]
    ls[a] = ls[b]
    ls[b] = c

def sort_pairs(pairs):
    unsorted = pairs.items()
    sorted = []

    for pair in unsorted:
        balanced = 0
        pair_index = len(sorted)
        sorted.append(pair)
        pair_frequency = pair[1]

        while not balanced and pair_index > 0:
            sort = sorted[pair_index - 1]
            if pair_frequency > sort[1]:
                swap(sorted, pair_index, pair_index - 1)
                pair_index -= 1
            else:
                balanced = 1

    return sorted

def sort_count(file):
    return sort_pairs(count_pairs(file))

