import math

class Convex:
    def __init__(self, between=(0.0, 1.0)):
        self.low, self.high = between

        if self.low > self.high:
            self.low, self.high = self.high, self.low

    def __repr__(self):
        return "|" + str(self.low) + " --- " + str(self.high) + "|"

    def set(self, between=(0.0, 1.0)):
        self.low, self.high = between

    def inBounds(self, val):
        return val >= self.low and val <= self.high

    def between(self):
        return self.high - self.low

    def ratio(self):
        return 1.0 / self.between()

    def toUnit(self, value):
        value = float(value)

        if value < self.low or value > self.high:
            value = ((value - self.low) % self.between()) + self.low

        return (value - self.low) / self.between()
        
    def fromUnit(self, value):
        if value < 0.0 or value > 1.0:
            value %= 1.0

        return (value * self.between()) + self.low

    def compose(self, convex):
        return Convex((convex.low + convex.between() * self.low, convex.low + convex.between() * self.high))

    def apply(self, convex):
        between = convex.low + self.low * convex.between(), convex.low + self.high * convex.between()
        self.set(between)

class NConvex:
    def __init__(self, ranges=[], convexes=[]):
        self.convexes = convexes[:]
        self.convexes.extend([Convex(between) for between in ranges])

    def __repr__(self):
        rep = ''

        for convex in self.convexes:
            rep += str(convex) + " "

        return rep

    def __len__(self):
        return len(self.convexes)

    def __getitem__(self, index):
        return self.convexes[index]

    def low(self):
        return [convex.low for convex in self.convexes]

    def high(self):
        return [convex.high for convex in self.convexes]

    def between(self):
        return [convex.between() for convex in self.convexes]

    def ratio(self):
        return [convex.ratio() for convex in self.convexes]

    def inBounds(self, point):
        inside = True
        index = 0

        while inside and index < len(point):
            inside = self.convexes[index].inBounds(point[index])
            index += 1

        return inside

    def toUnit(self, point):
        return [convex.toUnit(axis) for axis, convex in zip(point, self.convexes)]

    def fromUnit(self, point):
        return [convex.fromUnit(axis) for axis, convex in zip(point, self.convexes)]

    def compose(self, nconvex):
        return NConvex(convexes=[convex.compose(oconvex) for convex, oconvex in zip(self.convexes, nconvex.convexes)])

    def apply(self, nconvex):
        for convex, oconvex in zip(self.convexes, nconvex.convexes):
            convex.apply(oconvex)

class Lens:
    def __init__(self, red, blue):
        self.red = red
        self.blue = blue

    def fromRed(self, red):
        unitred = self.red.toUnit(red)
        blue = self.blue.fromUnit(unitred)

        return blue

    def fromBlue(self, blue):
        unitblue = self.blue.toUnit(blue)
        red = self.red.fromUnit(unitblue)

        return red

    def redRatio(self):
        return [float(red.between()) / blue.between() for red, blue in zip(self.red, self.blue)]

    def blueRatio(self):
        return [float(blue.between()) / red.between() for red, blue in zip(self.red, self.blue)]
    
class ZLens(Lens):
    def __init__(self, red, blue):
        Lens.__init__(self, red, blue)

    def fromRed(self, red):
        blue = Lens.fromRed(self, red)
        return [int(math.floor(bluebit)) for bluebit in blue]

    def fromBlue(self, blue):
        red = Lens.fromBlue(self, blue)
        return [int(math.floor(redbit)) for redbit in red]

    def redRatio(self):
        ratio = Lens.redRatio(self)
        return [int(math.floor(ratiobit)) for ratiobit in ratio]

    def blueRatio(self):
        ratio = Lens.blueRatio(self)
        return [int(math.floor(ratiobit)) for ratiobit in ratio]

    

def convextest():
    low, high = 12, 13.5

    pat = Convex((low, high))

    print "low -", pat.low, " :: high -", pat.high

    print "from 0.5: ", pat.fromUnit(0.5)
    print "to 12.5: ", pat.toUnit(12.5)

    if not pat.inBounds(12.8) or pat.inBounds(111.1):
        print "inBounds error"
    else:
        print "inBounds working"

    print "between: ", pat.between()
    print "composed with self: ", pat.compose(pat)

    pat.apply(pat)
    pat.apply(pat)

    print "applied to self twice: ", pat


def nconvextest():
    ranges = [(122, 1333.5), (-12.0, 14.33)]
    testfrom = (0.3, 0.2)
    testto = (500.0, 13.0)
    testout = (-99999.0, 22.0)

    ull = NConvex(ranges)

    print "low -", ull.low(), " :: high -", ull.high()

    print "from", testfrom, ":", ull.fromUnit(testfrom)
    print "to", testto,":", ull.toUnit(testto)

    if not ull.inBounds(testto) or ull.inBounds(testout):
        print "inBounds error"
    else:
        print "inBounds working"

    print "between: ", ull.between()
    print "composed with self: ", ull.compose(ull)

    ull.apply(ull)
    ull.apply(ull)

    print "applied to self twice: ", ull



def test():
    convextest()
    nconvextest()

#     jar = NConvex([(3.5, 9.222), (-12, 4444)])
#     tian = NConvex([(0.003, 0.0092), (222, 22222)])

#     print jar.toUnit((4.0, 1000))
#     print jar.fromUnit((0.2, 0.2))

#     puk = Lens(jar, tian)
    
#     spul = (4.1, 3888)
#     gin = puk.fromRed(spul)
    
#     print spul
#     print gin
#     print puk.fromBlue(gin)

#     print puk.blueRatio()
#     print puk.redRatio()

#     return puk
