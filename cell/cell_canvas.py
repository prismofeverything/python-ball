#!/usr/bin/python

import music
import sound
import interface
import math
import cell_base
import utility

from pygame.locals import *

class CellGram(interface.Gram):
    def __init__(self, rect, cell):
        interface.Gram.__init__(self, rect)

        self.cell = cell

    def hasChanged(self):
        return self.cell.hasChanged()

    def toggle(self):
        self.cell.toggle()

    def color(self):
        return self.cell.state.color

    def getDraws(self, full=False):
        draws = []

        if full or self.hasChanged():
            draws.append(interface.RectDraw(color=self.color()))

        return draws

    def makeDraw(self):
        return interface.RectDraw(self.rect(), self.color())

class CellCanvas(interface.Gram):
    def __init__(self,
                 rule,
                 rect=(0.0, 0.0, 1.0, 1.0),
                 dim=(9, 9),
                 delay=100,
                 scale=music.Scale([(1, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6), (8, 7), (9, 8), (10, 9), (11, 10)]),
                 basefreq=60.0):
        interface.Gram.__init__(self, rect)

        self.columns, self.rows = dim
        self.gridvex = utility.NConvex([(0, self.columns), (0, self.rows)])

        print "gridvex -- ", self.gridvex, "of len", len(self.gridvex)

        self.lens = utility.ZLens(self, self.gridvex)

        self.rule = rule
        self.grid = cell_base.CellGrid((self.columns, self.rows), self.rule)

        self.running = False
        self.delay = delay
        self.speed = 1
        self.toggled = []

        self.playing = False
        self.scale = scale
        self.basefreq = basefreq
        self.tones = {}
        self.tonesOn = set([])
        self.tonesChanged = set([])

        cratio, rratio = self.gridvex.ratio()

        self.boxes = [[self.addGram(self.makeBox((column, row), cratio, rratio))
                       for row in range(self.rows)]
                      for column in range(self.columns)]

    def activate(self, parentgram):
        interface.Gram.activate(self, parentgram)
        self.control = self.parentgram.getTimer(self.delay, self.run)

    def makeBox(self, pos, cratio, rratio):
        cell = self.grid.cellAt(pos)
        rect = (pos[0] * cratio, pos[1] * rratio, cratio, rratio)

        return CellGram(rect, cell)

    def boxAt(self, pos):
        return self.boxes[pos[0]%self.columns][pos[1]%self.rows]

    def cellAt(self, point):
        pos = self.lens.fromRed(point)
        return self.boxAt(pos)

    def setCell(self, pos, state):
        self.grid.setCell(pos, state)

    def setCells(self, cells, state):
        for cell in cells:
            self.setCell(cell, state)

    def getDraws(self, full=False):
        return []

    def findDraws(self, full=False):
        return [cell.makeDraw().applyBox(self) for cell in self.subgrams if full or cell.hasChanged()]

    def drawCells(self, full=False):
        draws = [cell.makeDraw().applyBox(self) for cell in self.subgrams if full or cell.hasChanged()]
        self.parentgram.trigger(draws)

    def setSpeed(self, speed):
        self.speed = speed

        fast = 9 - speed
        self.control.rate = self.delay = (2 ** fast) * (10.0 / 512)

    def generation(self, environment=None):
        gridtime = utility.timefunc(self.grid.generation)
        drawtime = utility.timefunc(self.drawCells)

        print "grid generation time:", gridtime
        print "cell drawing time:", drawtime

    def play(self):
        sound = self.getSound()

        liston = [len(group) for group in self.grid.groups if group.state != self.grid.rule.states[0]]

        seton = set(liston)
        newon = seton - self.tonesOn
        newoff = self.tonesOn - seton
        
        print seton
        print newon
        print newoff

        self.tonesChanged = newon | newoff
        
        for on in newon:
            on -= 1
            freq = self.scale.frequencyOf(on, self.basefreq)
            gain = 0.2

            if freq < 3001:
                tone = sound.sendToneOn(on, freq, gain)
                self.tones[on] = tone

            print "tone on:", str(on), "freq:", str(freq)
            
        for off in newoff:
            off -= 1

            if self.tones.has_key(off):
                self.tones.pop(off).off()

            print "tone off: " + str(off)

        self.tonesOn = seton


    def keydown(self, key):
        if key == K_ESCAPE:
            return "quit"

        elif key == K_SPACE:
            self.running = not self.running

            if self.running: print "running"
            else: print "stopped"

        elif key == K_RETURN:
            self.grid.randomize()
            self.drawCells()

        elif key == K_EQUALS:
            self.playing = not self.playing
            if not self.playing:
                self.getSound().allOff()

        elif key == K_1: self.setSpeed(1)
        elif key == K_2: self.setSpeed(2)
        elif key == K_3: self.setSpeed(3)
        elif key == K_4: self.setSpeed(4)
        elif key == K_5: self.setSpeed(5)
        elif key == K_6: self.setSpeed(6)
        elif key == K_7: self.setSpeed(7)
        elif key == K_8: self.setSpeed(8)
        elif key == K_9: self.setSpeed(9)
        elif key == K_0: self.setSpeed(0)

        return "ok"

    def mousedown(self, pos):
        interface.Gram.mousedown(self, pos)

        if self.inBounds(pos):
            self.toggled = []

            cell = self.cellAt(pos)
            cell.toggle()
            self.toggled.append(cell)

            cell.trigger()

    def mousedrag(self, lpos):
        interface.Gram.mousedrag(self, lpos)

        for pos in lpos:
            if self.inBounds(pos):
                cell = self.cellAt(pos)

                if not cell in self.toggled:
                    cell.toggle()
                    self.toggled.append(cell)
                    cell.trigger()

    def run(self, env=None):
        if self.running: self.generation()
        if self.playing: self.play()

    def quit(self, env=None):
        self.iface.quit()
        self.sound.allOff()

glider = [(0, 0), (1, 0), (2, 0), (2, 1), (1, 2)]

def random_pos(many, dim):
    return [(random.choice(range(dim[0])), random.choice(range(dim[1]))) for lll in range(many)]

def test():
    arect = (0.1, 0.1, 0.4, 0.3)
    brect = (0.5, 0.6, 0.3, 0.4)

    bdeath = utility.Color(hsl=(0.6, 0.3, 0.6))
    blife = utility.Color(hsl=(0.1, 0.7, 0.4))

    adim = (19, 19)
    bdim = (13, 13)
    miin = music.ScaleGenerator()

    iface = interface.Interface([500, 500])
    iface = iface

    ak = CellCanvas(cell_base.TumorRule(),
                    arect, adim,
                    delay=100, scale=miin.majorDiatonic().mode(1), basefreq=110.0)

    bk = CellCanvas(cell_base.LifeRule(bdeath, blife),
                    brect, bdim,
                    delay=100, scale=miin.majorDiatonic().mode(1), basefreq=220.0)

    canvii = [ak, bk]
    for canvas in canvii:
        iface.addGram(canvas)
        iface.addListener('mousedrag', canvas.mousedrag)
        canvas.drawCells(True)

    return iface

if __name__ == '__main__':
    mak = test()
    mak.start()

