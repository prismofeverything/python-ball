#!/usr/bin/python

from graphics import *
from cell import *

class CellCanvas:
    def __init__(self, rule, width, height, rows, columns):
        self.width = width
        self.height = height
        self.rows = rows
        self.columns = columns
        self.canvas = Interface(width = self.width, height = self.height)
        self.unit_width = (width // columns)
        self.unit_height = (height // rows)
        self.rule = rule
        self.cells = CellGrid(rows, columns, self.rule)
        self.rectangles = []
        for r in range(rows):
            row = []
            for c in range(columns):
                row.append(self.canvas.makeRect((r * self.unit_height),
                                                (c * self.unit_width),
                                                self.unit_width,
                                                self.unit_height))
            self.rectangles.append(row)
    def rectangleAt(self, p):
        return self.rectangles[p[0]%self.rows][p[1]%self.columns]
    def drawCells(self):
        for r in range(self.rows):
            for c in range(self.columns):
                cell = self.cells.cellAt([r,c])
                #if (cell.hasChanged()):
                self.canvas.drawRect(self.rectangleAt([r,c]), cell.state.color)
        self.canvas.update()
    def randomize(self, percentage):
        self.cells.randomize(percentage)
        self.drawCells()
    def generation(self, environment):
        self.cells.generation(environment)
        self.drawCells()
    def nGenerations(self, n, delay, environment):
        for i in range(n):
            if not self.cells.isStagnant:
                self.generation(environment)
                pygame.time.wait(delay)
