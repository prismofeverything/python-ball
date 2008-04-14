from listx import *

def spaces(n):
    space = ""
    for a in range(n):
        space += " "

    return space



# the Fract class is just a storage class for the results
# of a tree refraction.

class Fract:
    def __init__(self, node, store, duration, factors):
        self.node = node
        self.store = store
        self.duration = duration
        self.factors = factors

    def __repr__(self):
        rep = ""

        rep += str(self.store) + '\n'
        rep += str(self.duration) + '\n'
        rep += str(self.factors) + '\n'

        return rep

    def emerge(self):
        self.factors.reverse()
        return self




# the trick with this is that the duration is stored as a list of its divisions, from top to bottom.
# this way a triplet sixteenth in five time would go [5, 2, 3].  So really, these are relative durations
# waiting for a quantity that represents the duration of the whole to find its actual duration.
# Also, this way the durations [2, 2, 3, 5] and [2, 5, 3, 2] would be the same duration if applied to the
# same total duration, but they would group differently with other notes.








# this is the structure of a tree of divisions.
# store is the actual data that resides at each node.
# over is the parent node.  

class DivisionTree:
    def __init__(self, over, store):
        self.over = over
        self.divisions = []
        self.store = store

        self.merged = False
        self.merging = False

    def __repr__(self):
        def print_unit(unit, rep):
            space = spaces(unit.depth())

            rep += str(unit.store)
            rep += space + "duration: " + str(unit.duration()) + "\n"
            rep += space + "divisions: \n"

            for div in unit.divisions:
                rep = print_unit(div, rep)

            rep += "\n"
            return rep

        return print_unit(self, "")

    def __getitem__(self, index):
        return self.divisions[index]

    def __len__(self):
        return len(self.divisions)

    def divide(self, number):
        divisions = self.divisions[:number]
        divisionsLeft = number - len(divisions)

        self.divisions = [DivisionTree(self, self.store.divide(number))
                          for d in range(divisionsLeft)]

    def root(self):
        if self.isRoot(): return self
        else: return over.root()

    def depth(self):
        def d(unit, risen):
            if unit.over == None: return risen
            else: return d(unit.over, risen+1)
        
        return d(self, 0)

    def isRoot(self):
        return self.over == None

    def isLeaf(self):
        return self.divisions == []

    def path(self):
        def find_path(unit, p):
            if unit.isRoot(): return p
            else:
                index = unit.over.divisions.index(unit)
                p.append(index)

                return find_path(unit.over, p)

        return reverse(find_path(self, []))

    def find(self, path):
        if path == []:
            return self
        else:
            index = path[0]
            if index < 0:
                if self.isRoot(): return []
                else: return self.over.find(path[1:])
            elif index >= len(self.divisions):
                return []
            else:
                unit = self.divisions[index]
                return unit.find(path[1:])

    # bend and refract deal with transforming stores as they are drawn out of the tree.
    # all the leaves are extracted, which are then modified by their parents in an
    # additive way, so that each parent has the ability to influence the final form
    # of the leaf.  this plays the role of a set of nested contexts.

    # the final list is returned as a series of store/duration tuples, where the
    # duration is represented as a list of factors.  this list can be reduced by
    # multiplication to yield the total sliver of duration each leaf has.

    def bend(self, child):
        self.store.refract(child.store)
        child.duration.under *= len(self)
        child.factors.append(len(self))

        return child

    def refract(self):
        def fract(tree):
            if tree.isLeaf():
                return Fract(tree, tree.store.clone(), Ratio(1, 1), [])
            else:
                children = [fract(division) for division in tree.divisions]
                flatten(children)

                i = 0
                while i < len(children):
                    child = children[i]

                    if child.node.merging and i < len(children)-1:
                        merge = children.pop(i+1)

                        child.duration += merge.duration
                        child.node.merging = merge.node.merging
                    else:
                        i += 1

                return [tree.bend(child) for child in children]

        return [leaf.emerge() for leaf in fract(self)]

    # transform and traverse both modify nodes by a given function
    # transform applies the function to the whole tree
    # traverse only applies it to the leaves.

    def transform(self, morph):
        morph(self)
        for division in divisions:
            division.tranverse(morph)

    def traverse(self, morph):
        if self.isLeaf():
            morph(self)
        else:
            for division in self.divisions:
                division.traverse(morph)

    def leafnest(self):
        if self.isLeaf():
            return self
        else:
            return [division.leafnest() for division in self.divisions]

    def leaves(self):
        return flatten(self.leafnest())

    def set(self, path, store):
        if path == []:
            self.store.set(store)
        else:
            index = path[0]

            if index < 0:
                if self.isRoot():
                    self.generateOver(None, 2)
                self.over.set(path[1:], store)
            elif index >= len(self.divisions):
                self.divide(index+1)

            division = self.divisions[index]
            division.set(path[1:], store)

    def duration(self):
        def climb(unit, dur):
            if unit.isRoot(): return dur
            else:
                dur.append(len(unit.over.divisions))
                return climb(unit.over, dur)

        return reverse(climb(self, []))
        
    def generateOver(self, store, divisions):
        self.over = DivisionTree(None, store)
        self.over.divide(divisions)
        self.over.setChild(0, self)

    def setChild(self, index, child):
        self.divisions[index] = child

    def index(self):
        if self.isRoot():
            return 0
        else:
            return self.over.divisions.index(self)

    def isLastDivision(self):
        if self.isRoot():
            return true
        else:
            return self.index() == len(self.over)-1

    def isFirstDivision(self):
        if self.isRoot():
            return true
        else:
            return self.index() == 0

    # firstLeaf and lastLeaf are only relative to whatever root you provide.
    # if you want the absolute root, you need to call root, then first, as:
    #    node.root().first()
    #
    #  (or just use absfirstLeaf(), which I created after writing this comment)

    def firstLeaf(self):
        if self.isLeaf(): return self
        else: return self.divisions[0].firstLeaf()

    def lastLeaf(self):
        if self.isLeaf(): return self
        else: return self.divisions[len(self.divisions)-1].lastLeaf()

    def absfirstLeaf(self):
        return self.root().firstLeaf()

    def abslastLeaf(self):
        return self.root().firstLeaf()

    def nextLeaf(self):
        if self.isRoot():
            return self.lastLeaf()
        elif self.isLastDivision():
            return self.over.nextLeaf()            
        else:
            return self.over[self.index()+1].firstLeaf()

    def previousLeaf(self):
        if self.isRoot():
            return self.firstLeaf()
        elif self.isFirstDivision():
            return self.over.previousLeaf()
        else:
            return self.over[self.index()-1].lastLeaf()

    def merge(self):
        next = self.nextLeaf()

        if self != next: 
            self.merging = True
            next.merged = True

    def sever(self):
        next = self.nextLeaf()

        if self != next: 
            self.merging = False
            next.merged = False



