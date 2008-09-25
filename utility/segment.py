
class Convex:
    def __init__(self, low=0.0, high=1.0):
        self.low = low
        self.high = high

    def between(self):
        return self.high - self.low

    def toUnit(self, value):
        if value < self.low: return self.low
        elif value > self.high: return self.high

        return (value - self.low) / self.between()
        
    def fromUnit(self, value):
        return (value * self.between()) + self.low

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

    
