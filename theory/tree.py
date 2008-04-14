class Tree:
    def __init__(self, parent, value):
        self.parent = parent
        self.value = value
        self.children = []

    def divisions(self):
        return len(self.children)

    def divide(self, divisions):
        oldchildren = self.children
        self.children = []

        for d in range(divisions):
            if d < len(oldchildren):
                self.children.append(oldchildren[d])
            else:
                self.children.append(Tree(self, self.value.divide()))

    def access(self, index):
        if self.divisions <= index:
            self.divide(index+1)

        return self.children[index]

    def traverse(self, address):
        if not len(address): return self
        else:
            subtree = self.access(address[0])
            
            if len(address) == 1:
                return subtree
            else:
                return subtree.traverse(address[1:])

    def addBranch(self, address, branch):
        self.children.insert(address, branch)

    def removeBranch(self, address):
        self.children.remove(self.children[address])


class RhythmTree(Tree):
    
