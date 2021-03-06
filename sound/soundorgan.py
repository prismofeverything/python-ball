import sys, pygame
import math
import music
import sound

class SoundOrgan:
	def __init__(self, scale, basefreq):
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
		
		self.sound = sound.Sound()
		self.down = {}

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

	def sendKeyDown(self, key):
		tone = self.orderOf(key)
		freq = self.scale.frequencyOf(tone, self.basefreq)
		gain = 0.2

		tone = self.sound.sendToneOn(key, freq, gain)
		self.down[key] = tone

		print "down: " + str(key) + " at " + str(freq)

	def sendKeyUp(self, key):
		if self.down.has_key(key):
			self.down[key].off()
			self.down[key] = None

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



def start():
	hl = music.ScaleGenerator()
	ug = SoundOrgan(hl.worthy(), 200.0)

	ug.start()
