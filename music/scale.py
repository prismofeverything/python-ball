import math
from utility import Ratio

class Scale:
    def __init__(self, tones):
        self.tones = [Ratio(tone[0], tone[1]) for tone in tones]

    def __repr__(self):
        rep = ""

        for tone in self.tones:
            rep += str(tone) + " "

        return rep

    def __len__(self):
        return len(self.tones)

    def __getitem__(self, index):
        return self.tones[index]
        
    def normalize(self):
        for tone in self.tones:
            tone.normalize()

    def stepOf(self, tone):
        return self.tones.index(tone)

    def toneAt(self, step):
        return self.tones[step % len(self)]

    def order(self):
        self.tones.sort()
        return self

    def mode(self, mode):
        front = self.tones[mode:]
        back = self.tones[0:mode]

        return Scale(front + back)

    def invert(self):
        for tone in self.tones:
            tone.invert()
            tone.normalize()

        self.order()
        
    def merge(self, other):
        for tone in other:
            if not tone in self:
                self.tones.append(tone)

        return self.order()

    def symmetrify(self):
        inversion = Scale(self)
        inversion.invert()

        return self.merge(inversion)

    def frequencyOf(self, tone, basefreq):
        freq = 0.0

        if tone != None:
            octave = tone // len(self.tones)
            step   = tone  % len(self.tones)

            freq = basefreq * math.pow(2, octave)
            freq *= self.toneAt(step).value()

        return freq


class ScaleGenerator:
    def __init__(self):
        pass

    def otonality(self, order):
        tones = [(step, order) for step in range(order, order * 2)]
        return Scale(tones)

    def utonality(self, order):
        tones = [(order, step) for step in range(order, order * 2)]
        return Scale(tones).normalize()

    def majorPentatonic(self):
        tones = [(1,1), (9,8), (5,4), (3,2), (5,3)]
        return Scale(tones)

    def minorPentatonic(self):
        tones = [(1,1), (9,8), (6,5), (3,2), (8,5)]
        return Scale(tones)

    def majorDiatonic(self):
        tones = [(1,1), (9,8), (5,4), (4,3), (3,2), (5,3), (15,8)]
        return Scale(tones)

    def pureTwelve(self):
        tones = [(1,1), (16,15), (9,8), (6,5), (5,4), (4,3), (7,5), (3,2), (8,5), (5,3), (16,9), (15,8)]
        return Scale(tones)

    def worthy(self):
        tones = [(1,1), (33,32), (16,15), (11,10), (9,8), (8,7), (7,6), (6,5), (16,13), (5,4), (9,7), (4,3), (11,8),
                 (16,11), (3,2), (14,9), (8,5), (13,8), (5,3), (12,7), (7,4), (16,9), (20,11), (15,8), (64,33)]
        return Scale(tones)

    def extended(self):
        tones = [(1,1), (10,9), (9,8), (8,7), (7,6), (6,5), (16,13), (5,4), (9,7), (4,3), (11,8),
                 (16,11), (3,2), (14,9), (8,5), (13,8), (5,3), (12,7), (7,4), (16,9), (9,5)]
        return Scale(tones)

    def equalTemperament(self, steps):
        tones = [(math.pow(2.0, float(step) / steps), 1.0) for step in range(steps)]
        return Scale(tones)
    
    def compareEqualJust(self):
        return self.pureTwelve().merge(self.equalTemperament(12))

    def melded(self, max):
        tones = self.otonality(1)
        
        for step in range(2, max + 1):
            tones.merge(self.otonality(step))

        return tones

