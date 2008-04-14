#!/usr/bin/python

class Cell:
	def __init__(self, rule):
		self.rule = rule
		self.state = rule.empty()
		self.neighbors = []
		self.next_state = rule.empty()
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
		self.next_state = self.rule.apply(self.neighbors, environment)
		self.reset()
	def becomeNextState(self):
		self.state = self.next_state
	def findGroup(self, id, group):
		self.group_id = id
		self.included = 1
		group.append(self)
		for n in self.neighbors:
			if (not n.included) and n.state.id == self.state.id:
				n.findGroup(id, group)


class CellState:
	def __init__(self, id):
		self.id = id
	def __repr__(self):
		return str(self.id)

class GridCell(Cell):
	def __init__(self, rule, pos):
		Cell.__init__(self, rule)
		self.pos = pos

class CellGrid:
	def __init__(self, rows, columns, rule):
		self.grid = []
		self.columns = columns
		self.rows = rows
		self.rule = rule
		self.empty = rule.empty()
		self.groups = []
		for r in range(rows):
			row = [];
			for c in range(columns):
				row.append(GridCell(rule, (r, c)))
			self.grid.append(row)
		for r in range(rows):
			for c in range(columns):
				self.findNeighbors((r, c))
	def __repr__(self):
		rep = ""
		for r in range(self.rows):
			for c in range(self.columns):
				rep = rep+str(self.cellAt((r, c)))
			rep = rep+"\n"
		return rep
	def resetGrid(self):
		for r in range(self.rows):
			for c in range(self.columns):
				self.cellAt((r, c)).reset()
	def findNeighbors(self, p):
		cell = self.cellAt(p)
		for r in range(-1, 2):
			for c in range(-1, 2):
				cell.addNeighbor(self.cellAt((p[0]+r, p[1]+c)))
	def cellAt(self, pos):
		return self.grid[pos[0]%self.rows][pos[1]%self.columns]
	def setCell(self, pos, state):
		self.grid[pos[0]][pos[1]].state = state
	def findGroups(self, environment):
		group_id = 0
		group = []
		groups = []
		for r in range(self.rows):
			for c in range(self.columns):
				if not self.cellAt((r, c)).included:
					self.cellAt((r, c)).findGroup(group_id, group)
					groups.append(group)
					group = []
					group_id += 1
		return groups
	def generation(self, environment):
		for r in range(self.rows):
			for c in range(self.columns):
				self.cellAt((r, c)).determineNextState(environment)
		for r in range(self.rows):
			for c in range(self.columns):
				self.cellAt((r, c)).becomeNextState()
		self.groups = self.findGroups(environment)
					


class LifeRule:
	def __init__(self):
		self.death_state = CellState("death")
		self.life_state = CellState("life")
	def sumNeighbors(self, neighbors):
		sum = 0
		for cell in neighbors:
			if cell.state.id=="life":
				sum += 1
		return sum
	def empty(self):
		return self.death_state
	def apply(self, neighbors, environment):
		sum = self.sumNeighbors(neighbors)
		id = neighbors[4].state.id
		if id=="life":
			if sum < 3 or sum > 4:
				return self.death_state
			else:
				return self.life_state
		else:
			if sum == 3:
				return self.life_state
			else:
				return self.death_state


class BitRule:
	def __init__(self, rule):
		self.rule = rule
		self.ones = 0
		for g in range(512):
			self.ones += 2 ** g
		self.on_state = CellState("1")
		self.off_state = CellState("0")
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
	def empty(self):
		return self.off_state
	def apply(self, neighbors, environment):
		bit = 0
		for h in range(9):
			if neighbors[h].state.id == '1':
				if h < 4:	
					bit += 2 ** h
				elif h > 4:
					bit += 2 ** (h-1)
				else:
					bit += 2 ** 8
		if self.getBit(bit):
			return self.on_state
		else:
			return self.off_state

	

def life_test():
	rule = LifeRule()
	life = rule.life_state
	death = rule.death_state
	grid = CellGrid(3, 3, rule)
	grid.setCell((1, 1), life)
	grid.setCell((1, 2), life)
	grid.setCell((2, 1), life)
	print grid
	grid.generation("ehie")
	print grid
	
def bit_test():
	rule = BitRule(18950741984370598709517387387387873873871910345678951678358235879548757757575026262533443344343435262626262641836747644764748649105006506506506506509346116746595959)
        rule = BitRule(595959595111111111112637)
	on_state = rule.on_state
	off_state = rule.off_state
	grid = CellGrid(5, 5, rule)
	grid.setCell((3, 2), on_state)
	grid.setCell((4, 1), on_state)
	grid.setCell((4, 2), on_state)
	grid.setCell((4, 3), on_state)
	grid.setCell((2, 3), on_state)
	print grid
	grid.generation
	print grid


