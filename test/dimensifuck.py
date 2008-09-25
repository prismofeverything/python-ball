"""
  dimensifuck.py -- implements Dimensifuck.

  Copyright (C) 2006 Steven Wallace

  This software is provided 'as-is', without any express or implied
  warranty.  In no event will the authors be held liable for any damages
  arising from the use of this software.

  Permission is granted to anyone to use this software for any purpose,
  including commercial applications, and to alter it and redistribute it
  freely, subject to the following restrictions:

  1. The origin of this software must not be misrepresented; you must not
     claim that you wrote the original software. If you use this software
     in a product, an acknowledgment in the product documentation would be
     appreciated but is not required.
  2. Altered source versions must be plainly marked as such, and must not be
     misrepresented as being the original software.
  3. This notice may not be removed or altered from any source distribution.


  Some patches from Josiah Worcester
  Copyright (C) 2006 Josiah Worcester

  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  as published by the Free Software Foundation; either version 2
  of the License, or (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.
"""

from numarray import *
import sys

def dimensionSubstr(line):
    a = enumerate(line)
    try:
        b = a.next()
    except:
        return ["", line]
    try:
        while 1:
            if b[1] not in "0123456789": return [line[0:b[0]], line[b[0]:]]
            b = a.next()
            while b[1] != ".":
                if b[1] not in "0123456789": return [line[0:b[0]], line[b[0]:]]
                b = a.next()
            b = a.next()
            if b[1] == ".":
                return None #syntax error
    except:
        return [line[0:b[0]], ""]

class Dimensifuck:
    def __init__(self):
        self.dimensions = 0
        self.dimensionSizes = []
        self.matrix = array(type=Int8)
        self.tape = [0]
        self.pointer = 0
    def run(self, verbose=False):
        location = [0] * self.dimensions
        dimension = 0
        nextDimension = 0
        direction = 1
        while 1:
            op = self._getMatrixAt(location)
            if verbose:
                print "Location: ", location
                print "Opcode:", "+-.,<>=_^vX "[op]
            if op == 0:
                self.tape[self.pointer] = (self.tape[self.pointer] + 1) & 255
            elif op == 1:
		self.tape[self.pointer] = (self.tape[self.pointer] - 1) & 255
            elif op == 2:
                sys.stdout.write(chr(self.tape[self.pointer]))
            elif op == 3:
		try:
                	self.tape[self.pointer] = ord(sys.stdin.read(1))
		except:
			self.tape[self.pointer] = 0
            elif op == 4:
                self.pointer -= 1
                if self.pointer < 0:
                    self.tape = [0] + self.tape
                    self.pointer = 0
            elif op == 5:
                self.pointer += 1
                if self.pointer == len(self.tape):
                    self.tape.append(0)
            elif op == 6:
                nextDimension += 1
            elif op == 7:
                nextDimension -= 1
            elif op == 8:
                if self.tape[self.pointer]:
                    dimension = nextDimension
                    direction = 1
            elif op == 9:
                if self.tape[self.pointer]:
                    dimension = nextDimension
                    direction = -1
            elif op == 10:
                return self.tape[self.pointer]
            location[dimension] += direction
    def loadMatrix(self, code):
        self.dimensions = 0
        code = [dimensionSubstr(i) for i in code.split('\n')]
        lines = []
        for i, j in enumerate(code):
            if j is None:
                print "Syntax error on line ", i
                return False
            if j[0]:
                lines.append(j)
                self.dimensions = max(self.dimensions, j[0].count(".") + 2)
            else:
                lines[-1][1] += j[1]
        self.dimensionSizes = [0] * self.dimensions
        for i in xrange(len(lines)):
            lines[i][0] = [len(lines[i][1])] + [int(j) for j in lines[i][0].split(".")]
            lines[i][0] += [0] * (len(lines[i][0]) - self.dimensions)
        for i in xrange(self.dimensions):
            self.dimensionSizes[i] = max([a[0][i] + 1 for a in lines])
        for i in xrange(self.dimensions):
            self.matrix = array([-1], type=Int8)
            self.matrix.resize(self.dimensionSizes)
        for i in lines:
            location = list(i[0])
            location[0] = 0
            for j in i[1]:
                self._setMatrixAt(location, self._getValue(j))
                location[0] += 1
        
    def loadFile(self, filename):
        self.loadMatrix(file(filename, "r").read())

    def _getMatrixAt(self, location):
        for i in location:
            if i < 0:
                return 10
        try:
            return reduce(lambda x, y: x[y], location, self.matrix)
        except:
            return 10
    def _setMatrixAt(self, location, value):
        array = self.matrix
        while len(location) > 1:
            array = array[location[0]]
            location = location[1:]
        array[location[0]] = value
    def _getValue(self, char):
        return "+-.,<>=_^vX".find(char)
            
