#!/usr/bin/python

import math
import random
import utility

class Cell:
	def __init__(self, rule):
		self.rule = rule

		self.state = rule.empty()
		self.next_state = rule.empty()
		self.previous_state = rule.empty()

		self.neighbors = []
		self.density = 0

		self.group_id = -1
		self.included = 0

	def __repr__(self):
		return str(self.state.id)

	def reset(self):		
		self.group_id = -1
		self.included = 0

	def addNeighbor(self, neighbor):
		self.neighbors.append(neighbor)

	def determineNextState(self, environment):
		self.next_state = self.rule.apply(self, self.neighbors, environment)
		self.reset()

	def becomeNextState(self):
		self.previous_state = self.state
		self.state = self.next_state

	def hasChanged(self):
		return (self.previous_state.id != self.state.id)

	def toggle(self):
		self.previous_state = self.state
		self.state = self.rule.toggleState(self.state)

	def findGroup(self, id):
		self.group_id = id
		self.included = 1

		group = [self]
		totalDensity = 0
		self.density = 0

		for neighbor in self.neighbors:
			if not neighbor.included and neighbor.state.id == self.state.id:
				neighbor_group, density = neighbor.findGroup(id)

				if len(neighbor_group):
					group.extend(neighbor_group)

				totalDensity += density

			if neighbor.state.id == self.state.id:
				self.density += 1

		return group, self.density + totalDensity


class CellState:
	def __init__(self, id, color):
		self.id = id
		self.color = color

	def __repr__(self):
		return str(self.id)

	def __eq__(self, other):
		return self.id == other.id

	def rotate(self, rule):
		index = rule.states.index(self) + 1
		index %= len(rule.states)

		return rule.states[index]

class CellGroup:
	def __init__(self, id, state, members, density):
		self.id = id
		self.state = state
		self.members = members
		self.density = float(density) / len(members)

	def __getitem__(self, index):
		return self.members[index]

	def __len__(self):
		return len(self.members)

	def __repr__(self):
		return str(self.id) + " - " + \
		       str(self.state) + ": " + \
		       str(len(self.members)) + " members, " + \
		       str(self.density) + " density"

class GridCell(Cell):
	def __init__(self, rule, pos):
		Cell.__init__(self, rule)
		self.pos = pos

class CellGrid:
	def __init__(self, dimension, rule):
		self.grid = []

		self.dimension = dimension
		self.columns, self.rows = dimension

		self.rule = rule
		self.empty = rule.empty()
		self.groups = []

		self.isStagnant = False
		self.percentage = 0.5

		self.grid = [[GridCell(rule, (c, r)) for r in range(self.rows)] for c in range(self.columns)] 
		self.forEach(lambda cell, grid: self.findNeighbors(cell.pos))

	def __repr__(self):
		rep = ""

		for r in range(self.rows):
			for c in range(self.columns):
				rep = rep+str(self.cellAt((c, r)))
			rep = rep+"\n"

		return rep

	def forEach(self, func):
		for r in range(self.rows):
			for c in range(self.columns):
				func(self.cellAt((c, r)), self)

	def accEach(self, func, env):
		for r in range(self.rows):
			for c in range(self.columns):
				func(self,cellAt((c, r)), env)

		return env

	def andEach(self, pred):
		for r in range(self.rows):
			for c in range(self.columns):
				if not pred(self.cellAt((c, r))):
					return False
		return True

	def orEach(self, pred):
		for r in range(self.rows):
			for c in range(self.columns):
				if pred(self.cellAt((c, r))):
					return True
		return False

	def resetGrid(self):
		self.forEach(lambda cell, grid: cell.reset())

	def findNeighbors(self, p):
		cell = self.cellAt(p)
		cell.neighbors = [self.cellAt((p[0]+c, p[1]+r))
				  for c in range(-1, 2)
				  for r in range(-1, 2)
				  if not (c == 0 and r == 0)]


	def cellAt(self, pos):
		return self.grid[pos[0]%self.columns][pos[1]%self.rows]

	def setCell(self, pos, state):
		self.cellAt(pos).state = state

	def toggleCell(self, pos):
		self.cellAt(pos).toggle()

	def randomize(self):
		def randize(cell, grid):
			if random.random() < grid.percentage:
				cell.toggle()

		self.forEach(randize)
		self.isStagnant = False

	def findGroups(self, environment):
		self.groups = []
		self.group_id = 0

		def findGroup(cell, grid):
			if not cell.included:
				group, density = cell.findGroup(grid.group_id)
				grid.groups.append(CellGroup(grid.group_id, cell.state, group, density))
				grid.group_id += 1

		self.forEach(findGroup)

	def generation(self, environment=None):
		self.isStagnant = True

		def becomeNext(cell, grid):
			cell.becomeNextState()
			if cell.hasChanged(): grid.isStagnant = False

		self.forEach(lambda cell, grid: cell.determineNextState(environment))
		self.forEach(becomeNext)

		self.findGroups(environment)

		print(str(len(self.groups)) + " groups:  stagnant -- " + str(self.isStagnant))
		return self


class Rule:
	def __init__(self):
		self.states = [CellState(0, (0, 0, 0, 0))]
	def empty(self):
		return self.states[0]
	def toggleState(self, state):
		return self.states[(state.id+1)%len(self.states)]
	def apply(self, cell, neighbors, environment):
		return environment

class LifeRule(Rule):
	def __init__(self,
		     deathcolor=utility.Color(hsl=(0.8, 0.8, 0.2)),
		     lifecolor=utility.Color(hsl=(0.2, 0.4, 0.7))):
		self.states = [CellState(0, deathcolor),
			       CellState(1, lifecolor)]

		self.life = self.states[1]
		self.death = self.states[0]

	def apply(self, cell, neighbors, environment):
		density = 0
		for neighbor in neighbors:
			if neighbor.state.id == 1:
				density += 1

		if cell.state.id == self.life.id:
			if density < 2 or density > 3:
				return self.death
			else:
				return self.life
		else:
			if density == 3:
				return self.life
			else:
				return self.death


class TumorRule(Rule):
	def __init__(self,
		     deathcolor=utility.Color(hsl=(0.8, 0.8, 0.2)),
		     lifecolor=utility.Color(hsl=(0.2, 0.4, 0.7))):
		self.states = [CellState(0, deathcolor),
			       CellState(1, lifecolor)]

		self.life = self.states[1]
		self.death = self.states[0]

	def apply(self, cell, neighbors, environment):
		density = 0
		for neighbor in neighbors:
			if neighbor.state.id == 1:
				density += 1

		if cell.state.id == self.life.id:
			if density < 2 or density > 4:
				return self.death
			else:
				return self.life
		else:
			if density == 3:
				return self.life
			else:
				return self.death


class BitRuleInt(Rule):
	def __init__(self,
		     rule,
		     offcolor=utility.Color(hsl=(0.0, 0.0, 0.0)),
		     oncolor=utility.Color(hsl=(1.0, 1.0, 1.0))):
		self.rule = rule
		self.ones = 0
		for g in range(512):
			self.ones += 2 ** g
		self.states = [CellState(0, offcolor),
			       CellState(1, oncolor)]

	def __repr__(self):
		rep = ""
		g = 0
		for h in range(8):
			for v in range(64):
				g = h*64+v
				if self.getBit(g): rep += '1'
				else: rep += '0'
			rep += '\n'
		return rep

	def getBit(self, bit):
		return self.rule & (2 ** bit)

	def setBit(self, bit):
		self.rule |= 2 ** bit

	def clearBit(self, bit):
		self.rule &= (self.ones - 2 ** bit)

	def toggleBit(self, bit):
		if self.getBit(bit) == 0:
			self.setBit(bit)
		else:
			self.clearBit(bit)

	def apply(self, cell, neighbors, environment):
		bits = [neighbor.state.id for neighbor in neighbors]
		bits.append(cell.state.id)


		glyph = 0
		for power in range(len(bits)):
			bit = bits[power]

			if bit > 0:
				digit = len(self.states) ** power
				glyph += bit * digit

		return self.states[self.getBit(glyph)]


class BitRuleList(Rule):
	def __init__(self,
		     rule=0,
		     states=[CellState(0, utility.Color((0.0, 0.0, 0.0))),
			     CellState(1, utility.Color((250.0, 250.0, 250.0)))]):
		self.states = states
		self.rule = utility.lbase(rule, len(self.states))

		if len(self.rule) == 0:
			self.rule = [0 for x in range(len(self.states) ** 9)]

	def __repr__(self):
		rep = ""

		index = 0

		if len(self.states) == 2:
			for a in range(32):
				for b in range(16):
					index = (16 * a) + b
					if self.rule[g]: rep += '1'
					else: rep += '0'
				rep += '\n'
		else:
			for bit in self.rule:
				rep += str(bit)

		return rep

	def translateNumber(self, rep):
		return utility.lbase(rep, len(self.states))

	def setRule(self, rep):
		rule = self.translateNumber(rep)

		for bit in range(len(self.rule)):
			if bit < len(rule):
				self.rule[bit] = rule[bit]
			else:
				self.rule[bit] = 0

	def getBit(self, bit):
		return self.rule[bit]

	def setBit(self, bit):
		self.rule[bit] = 1

	def clearBit(self, bit):
		self.rule[bit] = 0

	def toggleBit(self, bit):
		self.rule[bit] ^= 1

	def apply(self, cell, neighbors, environment):
		bits = [neighbor.state.id for neighbor in neighbors]
		bits.append(cell.state.id)

		glyph = 0
		for power in range(len(bits)):
			bit = bits[power]

			if bit > 0:
				digit = len(self.states) ** power
				glyph += bit * digit

		return self.states[self.rule[glyph]]


large_number = 18950741984370598709517387387387873873871910345678951678358235879548757757575026262533443344343435262626262641836747644764748649105006506506506506509346116746595959

the_key = 595959595111111111112637

def life_test():
	rule = LifeRule()
	life = rule.states[1]
	death = rule.states[0]
	grid = CellGrid((3, 3), rule)
	grid.setCell((1, 1), life)
	grid.setCell((1, 2), life)
	grid.setCell((2, 1), life)
	print grid
	grid.generation("ehie")
	print grid

def bit_test():
#	rule = BitRule(large_number)
        #rule = BitRule(the_key)

	rul = BitRuleInt()
	print rul.translateNumber(5)
	rul.setRule(large_number)

	

	on_state = rul.states[1]
	off_state = rul.states[0]

	grid = CellGrid((5, 5), rul)
	grid.setCell((3, 2), on_state)
	grid.setCell((4, 1), on_state)
	grid.setCell((4, 2), on_state)
	grid.setCell((4, 3), on_state)
	grid.setCell((2, 3), on_state)

	print grid
	grid.generation('hfieh')
	print grid
	grid.generation('hiegfh')
	print grid

	return grid


