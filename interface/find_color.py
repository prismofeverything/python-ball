import utility
import graphics

Color = utility.Color


class Knob(graphics.Gram):
    def __init__(self, rect):
        graphics.Gram.__init__(self, rect)

    def getDraws(self, full=False):
        return [graphics.EllipseDraw(self.rect(), self.background)]

class Slider(graphics.Gram):
    def __init__(self, rect, orientation="horizontal"):
        graphics.Gram.__init__(self, rect)

        self.value = 0.0

        self.orientation = orientation
        self.groove = utility.Convex((0.1, 0.9))
        self.knob = Knob((rect.x(), rect.y, rect.height, rect.height))
        self.buffer = rect.height / 2
        self.staleBoxes = []

    def value(self):
        return self.toUnit(self.knobRect.x)

    def mousedown(self, pos):
        graphics.Gram.mousedown(self, pos)

        if self.inBounds(pos):
            self.knob.x = pos.x - self.buffer

            if self.knob.x < self.x + self.buffer:
                self.knob.x = self.x + self.buffer

    def mousedrag(self, pos):
        graphics.Gram.mousedrag(self, pos)

        if self.convex.inBounds(pos):
            self.knobrect.x() += self.mousedelta[0]

class FindColor(graphics.Gram):
    def __init__(self, iface, rect):
        self.color = Color((0.0, 0.0, 0.0))
        self.convex = utility.NConvex([(0.0, 1.0)])

        self.redSlider = Slider(iface, rect)
