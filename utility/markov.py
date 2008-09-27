import wheel
import operator
import text
import random

class MarkovNode:
    def __init__(self, data):
        self.data = data
        self.before = wheel.Wheel()
        self.after = wheel.Wheel()
        self.occurrences = 1
        self.begins = 0
        self.ends = 0

    def precede(self, node):
        self.after.add(node.data, 1)
        node.before.add(self.data, 1)

    def occur(self):
        self.occurrences += 1

    def begin(self):
        self.begins += 1

    def end(self):
        self.ends += 1
        
    def isBeginning(self):
        return self.begins > 0

    def isEnding(self):
        return self.ends > 0

    def forward(self):
        return self.after.spin()

    def backward(self):
        return self.before.spin()

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
    
    def has(self, word):
        return word in self.nodes.keys()

    def generateN(self, n):
        statement = []
        node = None

        for x in range(n):
            if not node:
                node = self.getBeginning()
            statement.append(node.data)
            choice = node.forward()

        return ' '.join(statement)

    def generate(self):
        statement = []
        ended = False
        node = self.getBeginning()

        while True:
            statement.append(node.data)
            choice = node.forward()
            
            if not choice:
                break

            node = self.nodes[choice]

        return ' '.join(statement)

    def expandFrom(self, word):
        if self.has(word):
            node = self.nodes[word]
            statement = [node.data]

            while not node.isBeginning():
                choice = node.backward()
                node = self.nodes[choice]
                statement.append(node.data)
            statement.reverse()

            node = self.nodes[word]
            
            while not node.isEnding():
                choice = node.forward()
                node = self.nodes[choice]
                statement.append(node.data)

            return ' '.join(statement)
        else:
            return self.generate()


if __name__ == '__main__':
    test_source = [("maybe", "this", "will", "make", "some", "kind", "of", "sense"),
                   ("this", "maybe", "sense", "maybe", "kind", "kind", "sense", "of", "this", "will", "maybe")]

    def test():
        jar = open("/home/omnibus/thackdai-herolinian-ardus-implosivus")
        mik = jar.read()
        apn = text.parseConversation(mik)

        gaa = MarkovChain()
        gaa.appendSource(apn)
        return gaa

