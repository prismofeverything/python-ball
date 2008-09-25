from scale import *
import utility

class Note:
    def __init__(self, key, step=0, octave=0):
        self.key = key
        self.step = step
        self.octave = octave

    def __repr__(self):
        rep = ""
        rep += "key: " + str(self.key) + "\n"
        rep += "step: " + str(self.step) + "\n"
        rep += "octave: " + str(self.octave) + "\n"

        return rep

    def clone(self):
        return Note(self.key, self.step, self.octave)

    def divide(self, divisions=0):
        return Note(self.key)

    def set(self, other):
        self.key = other.key
        self.step = other.step
        self.octave = other.octave

    def refract(self, child):
        child.step += self.step
        child.octave += self.octave

def test():
    yar = ScaleGenerator()
    uao = yar.otonality(11)
    nom = Note(uao)
    joq = utility.DivisionTree(None, nom)

    joq.divide(3)
    joq[1].divide(2)
    joq[0].store.step = 5
    joq.store.step = 3

    ob = joq.find([1,1])
    print ob.path()

    return joq


def listToNoteTree(notelist):
    skip


























## storelist contains elements with the properties:
##   duration      ---  of the type Interval

# def listToNoteTree(storelist):
#    if storelist == []: return UnitTree(0, None)
#    elif len(storelist) == 1: return UnitTree(0, storelist[0])
#    else:
#        factors = [uniqueFactorization(store.duration.under) for store in storelist]
#        for factor in factors: factor.reverse()

#        def max(a, b):
#            if not a: return b
#            if a > b: return a
#            else: return b

#        def highestFactor(fs, highest, ceiling):
#            if fs == []: return highest
#             else:
#                 underCeiling = [f for f in fs[0] if f < ceiling or ceiling == 0]
#                 return highestFactor(fs[1:], max(fs[0][0], highest), ceiling)

#        def isCommon(f, fs):
#            if fs == []: return True
#            elif not fs[0].contains(f): return False
#            else: return isCommon(f, fs[1:])

#        def removeFactor(f, fs):
#            return [[factor for factor in factors if factor != f] for factors in fs]

#        def findCommonFactors(fs):
           
#            def compareF(a, b):
#                if b[1] == a[1]: return a[0] < b[0]
#                else: return a[1] < b[1]
               
#            def extractCommon(fs, ceiling, common):
#                frequencies = {}
               
#                for factors in fs:
#                    for factor in factors:
#                        if not frequencies.keys().contains(factor):
#                         frequencies[factor] = 1
#                     else: frequencies[factor] += 1
                    
#                fpairs = [[(factor, freq) for factor in frequencies.keys()] for freq in frequencies.values()]
#                fpairs.sort(compareF) 
