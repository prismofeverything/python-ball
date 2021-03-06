def unitize(value):
    if value < 0.0: value += 1.0
    if value > 1.0: value -= 1.0

    return value

def rtoh(rgb):
    red, green, blue = rgb

    def colorDelta(color, ceiling, delta):
        return (((ceiling - color) / 6.0) + (delta / 2.0)) / delta

    base = min(rgb)
    ceiling = max(rgb)
    delta = ceiling - base
    gamma = ceiling + base

    hue = 0.0
    sat = 0.0
    lum = gamma / 2.0
    
    if delta > 0:
        if lum < 0.5: sat = delta / gamma
        else:         sat = delta / (2.0 - gamma)

        rdelta = colorDelta(red,   ceiling, delta)
        gdelta = colorDelta(green, ceiling, delta)
        bdelta = colorDelta(blue,  ceiling, delta)

        if   ceiling == red:   hue = bdelta - gdelta
        elif ceiling == green: hue = rdelta - bdelta + (1.0/3.0)
        elif ceiling == blue:  hue = gdelta - rdelta + (2.0/3.0)

    return (unitize(hue), sat, lum)

def htor(hsl):
    hue, sat, lum = hsl
    red = green = blue = lum

    if sat > 0.0:
        if lum < 0.5: b = lum * (1.0 + sat)
        else:         b = (lum + sat) - (sat * lum)

        a = 2.0 * lum - b
        onethird = 1.0/3.0

        def slice_hue(a, b, huecycle):
            huecycle = unitize(huecycle)

            if   6.0 * huecycle < 1.0: return a + ((b - a) * 6.0 * huecycle)
            elif 2.0 * huecycle < 1.0: return b
            elif 3.0 * huecycle < 2.0: return a + ((b - a) * 6.0 * ((2.0 / 3.0) - huecycle))
            else:                      return a

        red   = slice_hue(a, b, hue + onethird)
        green = slice_hue(a, b, hue)
        blue  = slice_hue(a, b, hue - onethird)

    return (red, green, blue)


class Color:
    def __init__(self,
                 rgb = (0.0, 0.0, 0.0),
                 alpha = 1.0,
                 hsl = (0.0, 0.0, 0.0)):
        self.red, self.green, self.blue = rgb
        self.hue, self.sat,   self.lum  = hsl
        self.alpha = alpha

        if hsl == (0.0, 0.0, 0.0):
            self.updateHSL()
        else:
            self.updateRGB()

    def __repr__(self):
        return str(self.hsla())

    def rgb(self):  return (self.red, self.green, self.blue)
    def rgba(self): return (self.red, self.green, self.blue, self.alpha)
    def hsl(self):  return (self.hue, self.sat,   self.lum)
    def hsla(self): return (self.hue, self.sat,   self.lum,  self.alpha)

    def rgba256(self): return [int(255 * component) for component in self.rgba()]

    def updateHSL(self): self.hue, self.sat,   self.lum  = rtoh(self.rgb())
    def updateRGB(self): self.red, self.green, self.blue = htor(self.hsl())

    def setRGB(self, rgb):
        self.red, self.green, self.blue = rgb
        self.updateHSL()

    def setRGBA(self, rgba):
        self.red, self.green, self.blue, self.alpha = rgba
        self.updateHSL()

    def setHSL(self, hsl):
        self.hue, self.sat, self.lum = hsl
        self.updateRGB()

    def setHSLA(self, hsla):
        self.hue, self.sat, self.lum, self.alpha = hsla
        self.updateRGB()

    def setRed(self, red):
        self.red = red
        self.updateHSL()

    def setGreen(self, green):
        self.green = green
        self.updateHSL()

    def setBlue(self, blue):
        self.blue = blue
        self.updateHSL()

    def setHue(self, hue):
        self.hue = hue
        self.updateRGB()

    def setSat(self, sat):
        self.sat = sat
        self.updateRGB()

    def setLum(self, lum):
        self.lum = lum
        self.updateRGB()

    def incRed(self, red):
        self.red += red
        if self.red > 1.0 or self.red < 0.0:
            self.red %= 1.0

        self.updateHSL()

    def incGreen(self, green):
        self.green += green
        if self.green > 1.0 or self.green < 0.0:
            self.green %= 1.0

        self.updateHSL()

    def incBlue(self, blue):
        self.blue += blue
        if self.blue > 1.0 or self.blue < 0.0:
            self.blue %= 1.0

        self.updateHSL()

    def incHue(self, hue):
        self.hue += hue
        if self.hue > 1.0 or self.hue < 0.0:
            self.hue %= 1.0

        self.updateRGB()

    def incSat(self, sat):
        self.sat += sat
        if self.sat > 1.0 or self.sat < 0.0:
            self.sat %= 1.0

        self.updateRGB()

    def incLum(self, lum):
        self.lum += lum
        if self.lum > 1.0 or self.lum < 0.0:
            self.lum %= 1.0

        self.updateRGB()

def test():
    red = (1.0, 0.0, 0.0)
    green = (0.0, 1.0, 0.0)
    blue = (0.0, 0.0, 1.0)

    ra = rtoh(red)
    ga = rtoh(green)
    ba = rtoh(blue)

    print ra, ga, ba


purple = Color(hsl=(0.8, 0.8, 0.2))
yellow = Color(hsl=(0.2, 0.4, 0.7))
