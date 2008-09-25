from math import *

import ossaudiodev
import array


format = ossaudiodev.AFMT_U8
speed = 8000
max_value = 255

# converts spectrum values (from -1.0 to 1.0) to
# an integer between 0 and 255

def convert(value):
    return int((value + 1.0) * (max_value / 2))


# append bytes or access the buffer to write data,
# then call cycle to write it to the soundcard

class Sound:
    def __init__(self):
        self.audio = ossaudiodev.open('rw')
        self.audio.setfmt(format)
        self.audio.channels(2)
        self.speed = self.audio.speed(speed)
        self.data = ''
        self.buffer = array.array('B')
        self.index = 0
    def append(self, value):
        self.buffer.append(convert(value))
    def reset(self):
        self.buffer = array.array('B')
    def cycle(self):
        self.data = self.buffer.tostring()
        self.audio.writeall(self.data)
    def close(self):
        self.audio.close()


sound = Sound()

class SineToneGenerator:
    def __init__(self, frequency=440, duration=1.0, amplitude=0.9):
        self.frequency = frequency
        self.duration = duration
        self.amplitude = amplitude
    def generate(self):
        sound.reset()
        for i in range(int(self.duration * sound.speed)):
            sound.append(self.amplitude *
                         sin((pi * self.frequency * i) / sound.speed))
        sound.cycle()
        

class Effect:
    def __init__(self, from_el, to_el):
        self.from_el = from_el
        self.to_el = to_el
    def affect(self):
        return self.from_el == self.to_el

class AddEffect(Effect):
    def __init__(self, from_el, to_el):
        Effect(from_el, to_el)
    def affect(self):
        self.to_el.next += self.from_el.value

class SubtractEffect(Effect):
    def __init__(self, from_el, to_el):
        Effect(from_el, to_el)
    def affect(self):
        self.to_el.next -= self.from_el.value

class ConditionEffect(Effect):
    def __init__(self, from_el, to_el):
        Effect(from_el, to_el)

class ToGreaterThanEffect(ConditionEffect):
    def __init__(self, from_el, to_el, value):
        ConditionEffect(from_el, to_el)
        self.value = value
    def affect(self):
        return (self.to_el.value > self.value)

class IfEffect(Effect):
    def __init__(self, from_el, to_el, condition, then, elsethen):
        Effect(from_el, to_el)
        self.condition = condition
        self.then = then
        self.elsethen = elsethen
    def affect(self):
        if self.condition.affect():
            self.then.affect()
        else:
            self.elsethen.affect()
            
    

class Element:
    def __init__(self, value):
        self.effects = []
        self.value = value
        self.next = value
    def addEffect(self, effect):
        self.effects.append(effect)
    def affect(self):
        for w in self.effects:
            w.affect()
    def react(self):
        self.value = self.next


class SineToneElementGroup:
    def __init__(self):
        self.elements = []
        self.elements.append(Element(0))
        self.elements.append(Element(5))
        self.elements.append(Element(1))
        a = self.elements[0]
        b = self.elements[1]
        c = self.elements[2]
        b.addEffect(AddEffect(b, a))
        c.addEffect(IfEffect(c, a, ToGreaterThanEffect(c, a, 0),
                                   SubtractEffect(c, b),
                                   AddEffect(c, b)))
    def value(self):
        return self.elements[0].value
    def cycle(self):
        for x in self.elements:
            x.affect()
        for l in self.elements:
            l.react()

class SineToneElementGenerator:
    def __init__(self, frequency=440, duration=1.0, amplitude=0.9):
        self.frequency = frequency
        self.duration = duration
        self.amplitude = amplitude
        self.group = SineToneElementGroup()
    def generate(self):
        sound.reset()
        for i in range(int(self.duration * sound.speed)):
            sound.append(self.group.value())
            self.group.cycle()
        sound.cycle()
