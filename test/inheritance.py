class A:
    def __init__(self, waka, wakainit=[]):
        self.waka = wakainit

        print "A waka = ", waka
        print "A wakainit =", wakainit

        self.waka.extend(waka)

        print "waka final -", self.waka

    def __repr__(self): return 'A'

    def allo(self):
        return [waka % 44.4 for waka in self.waka]

class B(A):
    def __init__(self, waka):
        print "B waka", waka

        A.__init__(self, waka)

    def __repr__(self): return 'B'

class C(B):
    def __init__(self, waka):
        print "C waka", waka

        A.__init__(self, waka)

    def __repr__(self): return 'C'

    def allo(self):
        return [waka % 777.77 for waka in self.waka]



def test():
    yam = C([33322, 99999999, 47474747])
    dog = B([9999888, 32492483, 1])
    lal = A([39393939, 247047204, 38383])

    print yam, yam.waka
    print dog, dog.waka
    print lal, lal.waka
