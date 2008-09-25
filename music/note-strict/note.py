import scale

def spaces(n):
    space = ""
    for a in range(n):
        space += " "

    return space


class Note:
    def __init__(self, key, duration=[], step=0, octave=0):
        self.key = key
        self.duration = duration
        self.step = step
        self.octave = octave

    def __repr__(self):
        space = spaces(len(self.duration))

        rep = ""
        rep += space + "key: " + str(self.key) + "\n"
        rep += space + "step: " + str(self.step) + "\n"
        rep += space + "octave: " + str(self.octave) + "\n"
        rep += space + "duration: " + str(self.duration) + "\n"

        return rep

    def divide(self, divisions):
        duration = self.duration[:]
        duration.append(divisions)

        return Note(self.key, duration)

    def set(self, other):
        self.key = other.key
        self.step = other.step
        self.octave = other.octave





class UnitTree:
    def __init__(self, over, store):
        self.over = over
        self.divisions = []
        self.store = store

        self.merged = 0
        self.merging = 0

    def __repr__(self):
        def print_unit(unit, rep):
            space = spaces(len(unit.duration()))
            
            rep += str(unit.store)
            rep += space + "divisions: \n"

            for div in unit.divisions:
                rep = print_unit(div, rep)

            rep += "\n"
            return rep

        return print_unit(self, "")

    def __getitem__(self, index):
        return self.divisions[index]

    def divide(self, number):
        divisions = self.divisions[:number]
        divisionsLeft = number - len(divisions)

        self.divisions = [UnitTree(self, self.store.divide(number)) for d in range(divisionsLeft)]

    def root(self):
        if unit.over == 0: return self
        else return over.root()

    def isLeaf(self):
        return self.divisions == []

    def path(self):
        def find_path(unit, p):
            if unit.over == 0: return p
            else:
                index = unit.over.divisions.index(unit)
                return find_path(unit.over, p.append(index))

        return find_path(self, []).reverse()

    def duration(self):
        def climb(unit, dur):
            if unit.over == 0: return dur
            else:
                dur.append(len(unit.over.divisions))
                return climb(unit.over, dur)

        dur = climb(self, [])
        dur.reverse()
        
        return dur
        
    def find(self, path):
        if path == []:
            return self
        else:
            index = path[0]
            if index < 0:
                if self.over == 0: return []
                else: return self.over.find(path[1:])
            elif index >= len(self.divisions):
                return []
            else:
                unit = self.divisions[index]
                return unit.find(path[1:])

    def set(self, path, store):
        if path == []:
            self.store.set(store)
        else:
            index = path[0]

            if index < 0:
                if self.over == 0:
                    self.over = UnitTree(self.key, 0)
                self.over.set(path[1:], unit)
            elif index >= len(self.divisions):
               self.divide(index+1)

            division = self.divisions[index]
            division.set(path[1:], store)

    def merge(self):
        next = self.next()

        if self != next: 
            self.merging = 1
            next.merged = 1

    def sever(self):
        next = self.next()

        if self != next: 
            self.merging = 0
            next.merged = 0

    def first(self):
        if self.isLeaf(): return self
        else: return self.divisions[0].first()

    def last(self):
        if self.isLeaf(): return self
        else: return self.divisions[len(self.divisions)-1].last()

    def next(self):
        if self.over == 0: return self
        else:
            index = self.over.divisions.index(self)

            if index == len(self.over.divisions) - 1:
                return self.over.next()
            else:
                return self.over[index + 1].first()

    def previous(self):
        if self.over == 0: return self
        else:
            index = self.over.divisions.index(self)

            if index == 0:
                return self.over.previous()
            else:
                return self.over[index - 1].last()










# storelist contains elements with the properties:
#   duration      ---  of the type Interval



























##
##def listToNoteTree(storelist):
##    if storelist == []: return UnitTree(0, None)
##    elif len(storelist) == 1: return UnitTree(0, storelist[0])
##    else:
##        factors = [scale.uniqueFactorization(store.duration.under) for store in storelist]
##        for factor in factors: factor.reverse()
##
##        def max(a, b):
##            if not a: return b
##            if a > b: return a
##            else: return b
##
##        def highestFactor(fs, highest, ceiling):
##            if fs == []: return highest
##             else:
##                 underCeiling = [f for f in fs[0] if f < ceiling or ceiling == 0]
##                 return highestFactor(fs[1:], max(fs[0][0], highest), ceiling)

##         def isCommon(f, fs):
##             if fs == []: return True
##             elif not fs[0].contains(f): return False
##             else: return isCommon(f, fs[1:])

##         def removeFactor(f, fs):
##             return [[factor for factor in factors if factor != f] for factors in fs]

##         def findCommonFactors(fs):

##             def compareF(a, b):
##                 if b[1] == a[1]: return a[0] < b[0]
##                 else: return a[1] < b[1]

##             def extractCommon(fs, ceiling, common):
##                 frequencies = {}

##                 for factors in fs:
##                     for factor in factors:
##                         if not frequencies.keys().contains(factor):
##                             frequencies[factor] = 1
##                         else: frequencies[factor] += 1

##                 fpairs = [(factor, freq) for factor in frequencies.keys() for freq in frequencies.values()]
##                 fpairs.sort(compareF) 
