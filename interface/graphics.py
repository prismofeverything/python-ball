#!/usr/bin/python

try:
    import sys
    import math
    import os
    import getopt
    import pyglet
    import time
    import utility
    import sound
    from interface.gl import *

except ImportError, err:
    print "couldn't load module:  %s" %(err)
    sys.exit(2)


def posdiff(apos, bpos):
    return [a - b for a, b in zip(apos, bpos)]

def scale(rect, factor):
    return rect[0], rect[1], rect[2] * factor, rect[3] * factor
    

class Side:
    def __init__(self, at, set, shift, tolerance=0.03):
        self.at = at
        self.set = set
        self.shift = shift
        self.tolerance = tolerance

    def __repr__(self):
        return str(self.at())

    def inside(self, pos):
        diff = pos - self.at()
        return abs(diff) <= self.tolerance

class Corner:
    def __init__(self, sides):
        self.sides = sides

    def __getitem__(self, index):
        return self.at()[index]

    def __len__(self):
        return len(self.sides)

    def __repr__(self):
        return str([side.at() for side in self.sides])

    def at(self):
        return [side.at() for side in self.sides]
        
    def set(self, pos):
        [side.set(to) for side, to in zip(self.sides, pos)]

    def shift(self, delta):
        [side.shift(to) for side, to in zip(self.sides, delta)]

    def inside(self, pos):
        return reduce(lambda within, (side, pos): within and side.inside(pos), zip(self.sides, pos), True)

class Box(utility.NConvex):
    def __init__(self, rect=(0, 0, 0, 0)):
        pos = rect[:2]
        dim = rect[2:]

        utility.NConvex.__init__(self, zip(pos, [p + d for p, d in zip(pos, dim)]))

        self.sides = [Side(self.left, self.setLeft, self.shiftLeft),
                      Side(self.top, self.setTop, self.shiftTop),
                      Side(self.right, self.setRight, self.shiftRight),
                      Side(self.bottom, self.setBottom, self.shiftBottom)]

        self.corners = [Corner((self.sides[a], self.sides[b])) for a, b in [(a, b) for a in (0, 2) for b in (1, 3)]]
        self.position = Side(self.pos, self.setPos, self.shiftPos)

    def box(self): return Box(self.rect())

    def x(self): return self.convexes[0].low
    def y(self): return self.convexes[1].low
    def width(self): return self.convexes[0].between()
    def height(self): return self.convexes[1].between()
    def left(self): return self.convexes[0].low
    def top(self): return self.convexes[1].low
    def right(self): return self.convexes[0].high
    def bottom(self): return self.convexes[1].high
    def pos(self): return self.x(), self.y()
    def dim(self): return self.width(), self.height()
    def rect(self): return self.x(), self.y(), self.width(), self.height()
    def zrect(self): return (int(math.ceil(self.x())),
                             int(math.ceil(self.y())),
                             int(math.ceil(self.width())),
                             int(math.ceil(self.height())))

    def setX(self, x): self.convexes[0].low = x
    def setY(self, y): self.convexes[1].low = y
    def setWidth(self, width): self.convexes[0].high = self.convexes[0].low + width
    def setHeight(self, height): self.convexes[1].high = self.convexes[1].low + height
    def setLeft(self, left): self.convexes[0].low = left
    def setTop(self, top): self.convexes[1].low = top
    def setRight(self, right): self.convexes[0].high = right
    def setBottom(self, bottom): self.convexes[1].high = bottom
    def setPos(self, pos):
        width, height = self.width(), self.height()

        self.setX(pos[0])
        self.setY(pos[1])
        self.setWidth(width)
        self.setHeight(height)
    def setDim(self, dim): self.setWidth(dim[0]), self.setHeight(dim[1])

    def setRect(self, rect):
        self.setX(rect[0])
        self.setY(rect[1])
        self.setWidth(rect[2])
        self.setHeight(rect[3])

    def shiftX(self, x): self.convexes[0].low += x
    def shiftY(self, y): self.convexes[1].low += y
    def shiftWidth(self, width): self.convexes[0].high += width
    def shiftHeight(self, height): self.convexes[1].high += height
    def shiftLeft(self, left): self.convexes[0].low += left
    def shiftTop(self, top): self.convexes[1].low += top
    def shiftRight(self, right): self.convexes[0].high += right
    def shiftBottom(self, bottom): self.convexes[1].high += bottom
    def shiftPos(self, pos):
        width, height = self.width(), self.height()

        self.shiftX(pos[0])
        self.shiftY(pos[1])
        self.setWidth(width)
        self.setHeight(height)

    def shiftDim(self, dim):
        self.shiftWidth(dim[0])
        self.shiftHeight(dim[1])

    def scale(self, factor):
        self.setDim([d * f for d, f in zip(self.dim(), factor)])

    def shiftRect(self, rect):
        self.shiftX(rect[0])
        self.shiftY(rect[1])
        self.shiftWidth(rect[2])
        self.shiftHeight(rect[3])

    def compose(self, box):
        composed = utility.NConvex.compose(self, box)
        return Box(composed.rect())

    def intersects(self, box):
        for corner in box.corners:
            if self.inBounds(corner):
                return True

        for corner in self.corners:
            if box.inBounds(corner):
                return True

        return False

class Draw(Box):
    def __init__(self, rect=(0.0, 0.0, 1.0, 1.0), color=utility.Color((0.0, 0.0, 0.0))):
        Box.__init__(self, rect)
        self.color = color

    def applyBox(self, box):
        self.apply(box)
        return self

    def draw(self, iface):
        pass

class RectDraw(Draw):
    def __init__(self, rect=(0.0, 0.0, 1.0, 1.0), color=utility.Color((0.0, 0.0, 0.0))):
        Draw.__init__(self, rect, color)

    def draw(self, iface):
        iface.drawRect(self.zrect(), self.color)

class EllipseDraw(Draw):
    def __init__(self, rect=(0.0, 0.0, 1.0, 1.0), color=utility.Color((0.0, 0.0, 0.0))):
        Draw.__init__(self, rect, color)

    def draw(self, iface):
        iface.drawEllipse(self.zrect(), self.color)

class TextDraw(Draw):
    def __init__(self,
                 text,
                 rect=(0.2, 0.3, 1.0, 1.0),
                 color=utility.Color((0.0, 0.0, 0.0))):
        Draw.__init__(self, rect, color)
        self.text = text
                
    def draw(self, iface):
        iface.drawText(self.zrect(), self.color, self.text)

class MultiDraw(Draw):
    def __init__(self,
                 draws=[],
                 rect=(0.0, 0.0, 1.0, 1.0),
                 color=utility.Color((0.0, 0.0, 0.0))):
        Draw.__init__(self, rect, color)
        self.draws = draws

    def addDraw(self, draw):
        self.draws.append(draw)

    def applyBox(self, box):
        Draw.applyBox(self, box)

        for draw in self.draws:
            draw.applyBox(box)

        return self

    def draw(self, iface):
        for d in self.draws:
            d.draw(iface)

class Gram(Box):
    def __init__(self, rect, background=utility.Color((0.0, 0.0, 0.0)), tolerance=0.03):
        Box.__init__(self, rect)

        self.parentgram = None
        self.subgrams = []
        
        self.focus = None
        self.background = background

        self.tolerance = tolerance
        self.mousepos = None

        self.resizing = False

    def activate(self, parentgram):
        self.parentgram = parentgram

    def addGram(self, subgram):
        self.subgrams.append(subgram)
        subgram.activate(self)

        return subgram

    def getUnique(self):
        if not self.parentgram: return -1
        else: return self.parentgram.subgrams.index(self)

    def getSound(self):
        if not self.parentgram:
            return None
        else:
            return self.parentgram.getSound()

    def getTimer(self, rate, func):
        return self.parentgram.getTimer(rate, func)

    def getDraws(self, full=False):
        return []

    def findDraws(self, full=False):
        draws = self.getDraws(full)

        for subdraw in [subgram.findDraws(full) for subgram in self.subgrams]:
            if len(subdraw):
                draws.extend(subdraw)                

        return [draw.applyBox(self) for draw in draws]

    def trigger(self, subdraws=[]):
        if not len(subdraws):
            subdraws = self.getDraws()

        self.parentgram.trigger([subdraw.applyBox(self) for subdraw in subdraws])

    def getMods(self):
        return self.parentgram.getMods()

    def rotateFocus(self, direction=1):
        if not self.focus:
            if len(self.subgrams):
                self.focus = self.subgrams[0]
        else:
            index = self.subgrams.index(self.focus)
            index += direction

            self.focus = self.subgrams[index % len(self.subgrams)]

    def keydown(self, key):
        mods = self.getMods()
        shiftdown = mods & KMOD_LSHIFT or mods & KMOD_RSHIFT

        if key == K_TAB:
            direction = 1
            if shiftdown: direction = -1

            self.rotateFocus(direction)

        if self.focus:
            return self.focus.keydown(key)
        else:
            for gram in self.subgrams:
                ret = gram.keydown(key)

                if ret == "quit":
                    return ret

    def keyup(self, key):
        if self.focus:
            self.focus.keyup(key)
        else:
            for gram in self.subgrams:
                gram.keyup(key)

    def resize(self, oldbox):
        pass  # meant to be overridden

    def mousedown(self, pos):
        self.shifting = None
        self.focus = None

        inbounds = False
        
        if self.inBounds(pos):
            inbounds = True

            mods = self.getMods()
            shiftdown = mods & KMOD_LSHIFT or mods & KMOD_RSHIFT

            for gram in self.subgrams:
                if gram.mousedown(pos):
                    self.focus = gram

            if shiftdown:
                for corner in self.corners:
                    if corner.inside(pos):
                        self.shifting = corner
                        self.resizing = True

                    if not self.resizing:
                        self.shifting = self.position

            if self.shifting:
                print "in corner", self.shifting

        self.mousepos = pos
        return inbounds

    def mouseup(self, pos):
        self.shifting = None
        self.mousedelta = None
        self.resizing = False

        self.mousepos = pos

        for sub in self.subgrams:
            sub.mouseup(pos)

    def mousedrag(self, pos):
        if len(pos):
            pos = pos[-1]
            self.mousedelta = posdiff(pos, self.mousepos)

            mods = self.getMods()
            shiftdown = mods & KMOD_LSHIFT or mods & KMOD_RSHIFT

            if self.shifting and shiftdown:
                oldbox = RectDraw(scale(self.rect(), 1.01), self.background)

                self.shifting.shift(self.mousedelta)
                if self.resizing:
                    self.resize(oldbox)

                self.parentgram.trigger([oldbox] + self.findDraws(True))



            self.mousepos = pos

    def mousemotion(self, pos):
        if len(pos):
            pos = pos[-1]

            self.mousedelta = posdiff(pos, self.mousepos)
            self.mousepos = pos
        


class Timer:
    def __init__(self, rate, func):
        self.rate = rate
        self.func = func
        self.clock = 0.0
        self.before = time.time()

    def __call__(self, elapsed):
        self.forward(elapsed)

    def forward(self, elapsed):
        self.clock += elapsed
        if self.clock > self.rate:
            self.clock = 0.0
            self.func()

class InterfaceListener:
    def __init__(self):


class InterfaceGlontrol(Glontrol):
    def __init__(self):
        Glontrol.__init__(self, 'interface')

        self.listeners = {}
        self.mouseDown = False

        for key in ['close',
                    'update',
                    'key_press',
                    'key_release',
                    'mouse_press',
                    'mouse_release',
                    'mouse_motion',
                    'mouse_drag']:
            self.listeners[key] = []

    def send(self, listener, *signal):
        for receptor in self.listeners[listener]:
            receptor.signal(listener, signal)

    def on_close(self): self.send('close')
    def on_update(self, dt): self.send('update', dt)
    def on_key_press(self, sym, mods): self.send('key_press', sym, mods)
    def on_key_release(self, sym, mods): self.send('key_release', sym, mods)
    def on_mouse_press(self, x, y, b, mods): self.send('mouse_press', x, y, b, mods)
    def on_mouse_release(self, dt): self.send('mouse_release', )
    def on_mouse_motion(self, dt): self.send('mouse_motion', [dt])
    def on_mouse_drag(self, dt): self.send('mouse_drag', [dt])

class Interface(Gram):
    def __init__(self, dimension, framerate=40, controlrate=0.2):
        Gram.__init__(self, (0, 0, dimension[0], dimension[1]))

        self.initializeGl()

        self.grams = []

        self.runclock = 0.0
        self.framerate = framerate
        self.previousTick = time.time()

        self.sound = sound.Sound()

    def initializeGl(self):
        self.ww = Glindow()
        self.ww.activeGlye().tz = -8

        self.glye = Glye(rotate_glye)
        self.glye.tz = -4

        self.glights = [Glight(GL_LIGHT0, vec(.5, .5, 1, 0), vec(.5, .5, 1, 1), vec(1, 1, 1, 1)),
                        Glight(GL_LIGHT1, vec(1, 0, .5, 0), vec(.5, .5, .5, 1), vec(1, 1, 1, 1))]

        self.glontrol = InterfaceGlontrol()

        self.ww.addGlye(glye)
        self.ww.glorld.glights = glights

        self.ww.addGlontrol(self.glontrol)
        self.glontrol.attach(self.ww)

        self.ww.start()

    def trigger(self, subdraws):
        boxes = []

        for subdraw in subdraws:
            subdraw.applyBox(self)
            subdraw.draw(self)
            boxes.append(self.makeRect(subdraw.zrect()))

        self.update(boxes)

    def getSound(self):
        return self.sound

    def getTimer(self, rate, func):
        return self.addTimer(rate, func)

    def makeRect(self, rect):
        return pygame.Rect(rect[0], rect[1], rect[2], rect[3])

    def drawRect(self, rect, color):
        return self.surface.fill(color.rgba256(), self.makeRect(rect))

    def drawEllipse(self, rect, color):
        pygame.draw.ellipse(self.surface, color.rgba256(), self.makeRect(rect)) 

    def drawText(self, rect, color, text):
        textimage = self.font.render(text, True, color.rgba256())
        self.surface.blit(textimage, self.makeRect(rect))

    def update(self, boxes=None):
        pygame.display.update(boxes)

    def getEvent(self):
        return pygame.event.get()

    def getMods(self):
        return pygame.key.get_mods()

    def tick(self, delay):
        pygame.time.delay(delay)

    def broadcast(self, channel, message):
		for listener in self.listeners[channel]:
			listener(message)

    def addListener(self, channel, listener):
        self.listeners[channel].append(listener)

    def addTimer(self, rate, func):
        timer = Timer(rate, func)
        self.listeners['timer'].append(timer)

        return timer

    def eventLoop(self):
        self.previousTick = time.time()

        while 1:
            mousemotion = []
            mousedrag = []

            for event in getEvent():
                if event.type == QUIT:
                    self.broadcast('quit', None)
                    return

                elif event.type == KEYDOWN:
                    if self.keydown(event.key) == "quit":
                        return

                elif event.type == KEYUP:
                    self.keyup(event.key)

                elif event.type == MOUSEBUTTONDOWN:
                    self.mouseDown = True

                    pos = self.toUnit(event.pos)
                    self.mousedown(pos)

                elif event.type == MOUSEBUTTONUP:
                    self.mouseDown = False

                    pos = self.toUnit(event.pos)
                    self.mouseup(pos)

                elif event.type == MOUSEMOTION:
                    pos = self.toUnit(event.pos)

                    if self.mouseDown:
                        mousedrag.append(pos)
                    else:
                        mousemotion.append(pos)

            if len(mousemotion):
                self.broadcast("mousemotion", mousemotion)
            if len(mousedrag):
                self.broadcast("mousedrag", mousedrag)

            now = time.time()
            elapsed = now - self.previousTick
            self.previousTick = now

            self.broadcast("timer", elapsed)

            self.tick(self.framerate)

    def start(self):
        self.eventLoop()

    def quit(self):
        pygame.display.quit()
        pygame.quit()
