import sys
import math
import music
import utility
import graphics

class RatioBox(graphics.Gram):

    def __init__(self,
                 order,
                 lens,
                 rect,
                 textcolor,
                 activecolor):
        graphics.Gram.__init__(self, rect)

        self.order = order
        self.lens = lens
        self.textcolor = textcolor
        self.activecolor = activecolor
        self.inactivecolor = utility.Color((0.0, 0.0, 0.0))

        self.pushed = False

    def makeDraw(self):
        rect = self.rect()
        x, y, width, height = rect
        textrect = (x+width*0.4, y+height*0.3, width*0.5, height*0.4)
        ratio = self.lens.findRatio(self.order)
        box = graphics.EllipseDraw(rect, self.inactivecolor)
        text = graphics.TextDraw(str(ratio), textrect, self.activecolor)
        
        if self.pushed:
            box.color = self.activecolor
            text.color = self.textcolor

        draws = [box, text]
        return graphics.MultiDraw(draws)

    def push(self):
        self.pushed = True

    def depush(self):
        self.pushed = False

textcolor = utility.Color((0.0, 0.1, 0.2))
activecolor = utility.Color((0.7, 0.8, 0.6))

class IOrgan(graphics.Gram):

    def __init__(self, scale, basefreq, rect=(0.0, 0.0, 1.0, 1.0)):
        graphics.Gram.__init__(self, rect)

        self.scale = scale
        self.basefreq = basefreq

        self.down = {}
        self.keyorder = [49, 113, 97, 122,
                         50, 119, 115, 120,
                         51, 101, 100, 99,
                         52, 114, 102, 118,
                         53, 116, 103, 98,
                         54, 121, 104, 110,
                         55, 117, 106, 109,
                         56, 105, 107, 44,
                         57, 111, 108, 46,
                         48, 112, 59, 47,
                         45, 91, 39]

        self.rboxes = []
        
        x = 0.0
        y = 0.0

        unitw = 0.08
        unith = 0.13

        xunit = 0
        yunit = 0

        for k in range(len(self.keyorder)):
            xpad = float(yunit) * (unitw / 7.0)
            newx = x + xpad + (unitw * xunit)
            newy = y + (unith * yunit)

            rbox = RatioBox(k,
                            self,
                            (newx, newy, unitw, unith),
                            textcolor,
                            activecolor)

            self.addGram(rbox)
            self.rboxes.append(rbox)

            yunit += 1
            if yunit > 3:
                yunit = 0
                xunit += 1

    def drawRatios(self):
        draws = [rbox.makeDraw().applyBox(self) for rbox in self.rboxes]
        self.parentgram.trigger(draws)

    def orderOf(self, key):
        try:
            tone = self.keyorder.index(key)
        except ValueError:
            tone = None
        return tone

    def fkeyOf(self, key):
        if key >= 282 and key < 294:
            return key - 282
        else:
            return None

    def findRatio(self, order):
        return self.scale.toneAt(order)

    def getDraw(self, tone):
        return self.rboxes[tone].makeDraw()

    def push(self, tone):
        if not tone == None:
            self.rboxes[tone].push()
            self.trigger([self.getDraw(tone)])

    def depush(self, tone):
        if not tone == None:
            self.rboxes[tone].depush()
            self.trigger([self.getDraw(tone)])

    def keydown(self, key):
        tone = self.orderOf(key)

        if tone == None:
            fkey = self.fkeyOf(key)

            if fkey == None:
                print str(key) + " is not a key"
            else:
                self.getSound().sendInstrumentChange(fkey)

        else:
            freq = self.scale.frequencyOf(tone, self.basefreq)
            gain = 0.8
            toneon = self.getSound().sendToneOn(key, freq, gain)

            self.down[key] = toneon
            print "down: " + str(key) + " at " + str(freq)

            self.push(tone)

    def keyup(self, key):
        if self.down.has_key(key):
            up = self.down.pop(key)
            up.off()

            print "up: " + str(key)

        tone = self.orderOf(key)
        self.depush(tone)

def test():
    hl = music.ScaleGenerator()
    mn = (0.0, 0.2, 1.0, 1.0)
    ug = IOrgan(hl.otonality(16), 100.0, mn)
    ak = graphics.Interface((1100, 300))
    ak.addGram(ug)

    ug.drawRatios()

    return ak



if __name__ == "__main__":
    ya = test()
    ya.start()
