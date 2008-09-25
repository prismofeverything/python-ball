#!/usr/bin/python

import pygame


class KeyState:
	def __init__(self, dimension=(400, 400)):
		pygame.init()
		self.surface = pygame.display.set_mode(dimension)

		self.keys_down = [0 for x in range(512)]
		self.listeners = []

	def addListener(self, listener):
		self.listeners.append(listener)

	def removeListener(self, listener):
		self.listeners.remove(listener)

	def sendKeyDown(self, event):
		self.keys_down[event.key] = 1
		
		for listener in self.listeners:
			listener.keyDown(event, self)

	def sendKeyUp(self, event):
		self.keys_down[event.key] = 0
		
		for listener in self.listeners:
			listener.keyUp(event, self.keys_down)

	def start(self):
		while 1:
			event = pygame.event.wait()
			
			if event.type == pygame.QUIT:
				quit()
			elif event.type == pygame.KEYDOWN:
				self.sendKeyDown(event)
			elif event.type == pygame.KEYUP:
				self.sendKeyUp(event)

	def quit(self):
		pygame.display.quit()
		pygame.quit()


class PrintKey:
	def __init__(self):
		pass

	def keyDown(self, event, keystate):
		print str(event.key) + " down"

	def keyUp(self, event, keystate):
		print str(event.key) + " up"



def test():
	pkd = PrintKey()
	anld = KeyState()
	anld.addListener(pkd)

	return anld



