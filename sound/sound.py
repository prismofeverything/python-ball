import osc
import math
import music

class ToneOn:
	def __init__(self, sound, unique, key, freq, gain):
		self.sound = sound

		self.key = key
		self.freq = freq
		self.gain = gain

		self.unique = unique

	def off(self):
		self.sound.sendToneOff(self.unique)

class Sound:
	def __init__(self):
		self.on = {}
		self.open = [n for n in range(1024, -1, -1)]
		self.instrument = 0

		osc.init()

	def sendToneOn(self, tone, freq, gain):
		unique = self.open.pop()
		osc.sendMsg('/keydown', [unique, freq, gain], "127.0.0.1", 9000)

		toneon = ToneOn(self, unique, tone, freq, gain)
		self.on[unique] = toneon

		return toneon

	def sendToneOff(self, unique):
		osc.sendMsg('/keyup', [unique], "127.0.0.1", 9000)

		if self.on.has_key(unique):
			self.on.pop(unique)
		self.open.append(unique)

	def sendInstrumentChange(self, to):
		osc.sendMsg('/instrumentchange', [to], "127.0.0.1", 9000)
		self.instrument = to

	def allOff(self):
		for tone in self.on.values():
			tone.off()
