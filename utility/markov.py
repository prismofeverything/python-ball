import wheel
import operator
import text
import random

class MarkovNode:
    def __init__(self, data):
        self.data = data
        self.following = wheel.Wheel()
        self.occurrences = 1
        self.begins = 0
        self.ends = 0

    def precede(self, node):
        self.following.add(node.data, 1)

    def occur(self):
        self.occurrences += 1

    def begin(self):
        self.begins += 1

    def end(self):
        self.ends += 1
        
    def choose(self):
        return self.following.spin()


class MarkovChain:
    def __init__(self):
        self.nodes = {}
        self.beginnings = wheel.Wheel()
        self.endings = []
        self.totalAtoms = 0
        self.totalGroups = 0
        self.averageGroup = 0
        self.maxGroupLength = 300
        self.endFactor = 3

    def appendSource(self, source):
        self.totalGroups += len(source)

        for group in source:
            self.totalAtoms += len(group)

            prenode = None
            node = None

            for atom in group:
                if self.nodes.has_key(atom):
                    node = self.nodes[atom]
                    node.occur()
                else:
                    node = MarkovNode(atom)
                    self.nodes[atom] = node

                if prenode:
                    prenode.precede(node)
                else:
                    node.begin()
                    self.beginnings.add(node.data, 1)

                prenode = node

            if node:
                node.end()
                self.endings.append(node)
        
        if self.totalGroups != 0:
            self.averageGroup = self.totalAtoms / self.totalGroups

    def getBeginning(self):
        beginning = self.beginnings.spin()
        return self.nodes[beginning]
    
    def generate(self):
        statement = []
        ended = False
        node = self.getBeginning()

        while not ended and len(statement) < self.maxGroupLength:
            statement.append(node.data)
            choice = node.choose()
            
            if not choice:
                return statement

            node = self.nodes[choice]

            if node.ends > 0:
                endChance = (self.endFactor * node.ends) / self.totalAtoms 
                if random.random() < endChance:
                    ended = True

        return ' '.join(statement)

test_source = [("maybe", "this", "will", "make", "some", "kind", "of", "sense"),
               ("this", "maybe", "sense", "maybe", "kind", "kind", "sense", "of", "this", "will", "maybe")]


def test():
    jar = open("/home/omnibus/thackdai-herolinian-ardus-implosivus")
    mik = jar.read()
    apn = text.parseConversation(mik)

    gaa = MarkovChain()
    gaa.appendSource(apn)
    return gaa

