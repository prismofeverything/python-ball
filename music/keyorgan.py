import sys, osc, pygame
import math
from scale import *

class KeyOrgan:
	def __init__(self, scale, basefreq):
		osc.init()
		pygame.init()

		self.size = self.width, self.height = 300, 300
		self.screen = pygame.display.set_mode(self.size)
		self.scale = scale
		self.basefreq = basefreq

		self.keyorder = [96, 9,
				 49, 113, 97, 122,
				 50, 119, 115, 120,
				 51, 101, 100, 99,
				 52, 114, 102, 118,
				 53, 116, 103, 98,
				 54, 121, 104, 110,
				 55, 117, 106, 109,
				 56, 105, 107, 44,
				 57, 111, 108, 46,
				 48, 112, 59, 47,
				 45, 91, 39,
				 61, 93, 13,
				 8, 92]
		
	def quit(self):
		pygame.display.quit()
		pygame.quit()
		sys.exit()

	def orderOf(self, key):
		try:
			tone = self.keyorder.index(key)
		except ValueError:
			tone = None

		return tone

	def keyToFreq(self, key):
		tone = self.orderOf(key)
		freq = 0.0

		if tone != None:
			octave = tone // len(self.scale)
			step = tone % len(self.scale)

			freq = self.basefreq * math.pow(2, octave)
			freq *= self.scale.toneAt(step).value()

		return freq

	def sendKeyDown(self, key):
		freq = self.keyToFreq(key)
		osc.sendMsg('/keydown', [key, freq], "127.0.0.1", 9000)
		print "down: " + str(key) + " at " + str(freq)

	def sendKeyUp(self, key):
		osc.sendMsg('/keyup', [key], "127.0.0.1", 9000)
		print "up: " + str(key)

	def start(self):
		while 1:
			event = pygame.event.wait()
			
			if event.type == pygame.QUIT:
				self.quit()
				return
			elif event.type == pygame.KEYDOWN:
				self.sendKeyDown(event.key)
			elif event.type == pygame.KEYUP:
				self.sendKeyUp(event.key)


def test():
	hl = ScaleGenerator()
	ug = KeyOrgan(hl.majorDiatonic(), 60.0)

	return ug
