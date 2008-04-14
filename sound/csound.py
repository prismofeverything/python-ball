import random
import re


# ---------------------------------------------------------------------------
# here are the globals.  an instance of class Random for undefined parameters,
# a regular expression for parsing parameter strings,
# and a global value to consistently identify open fields.  
# --------------------------------------------------------

omn = random.Random()

parameterPattern = re.compile("([ikax])([a-z]*)(?:,([0-9]*(?:.[0-9]*)?))?(?:,(-?[0-9]*(?:.[0-9]*)?))?")

open_field = 'o'

# --------------------------------------------------------------------
# class Parameter.  this is used to store information specific to each 
# parameter, such as its maximum rate, the value of its field, and the limits
# of the range of values it can be.  this can be used to connect an output to 
# the parameter in the appropriate way.
# ----------------------------------------------------

class Parameter:
	def __init__(self, rate='i',
			   description='',
			   range=1.0,
			   offset=0.0,
			   field=open_field):
		self.rate = rate
		self.field = field
		self.range = range
		self.offset = offset
		self.description = description
	def __repr__(self):
		return self.field
	def isOpen(self):
		return self.field == open_field
	def setField(self, field):
		self.field = field
	
class ParameterTranslator:
	def __init__(self, rate='i',
			   description='',
			   range=1.0,
			   offset=0.0,
			   field=open_field):
		self.rate = rate
		self.field = field
		self.range = range
		self.offset = offset
		self.description = description
	def parameter(self, parameterString):
		param = parameterPattern.match(parameterString).groups()
		rate = self.rate
		description = self.description
		range = self.range
		offset = self.offset
		if param[0]: rate = param[0]
		if param[1]: description = param[1]
		if param[2]: range = float(param[2])
		if param[3]: offset = float(param[3])
		return Parameter(rate, description, range, offset)
		
translator = ParameterTranslator()

# ---------------------------------------------------------------------------	
# ParameterList is a collection of Parameters and is mostly used to deal with
# optional parameters.  specifically, it makes sure that length() returns the
# length of the actual parameters being used, and not the potentially but not
# yet used, and that indexing works in the same way.  in order to expand the
# optional parameters, call expandOptions(x) and the parameters will unfold one 
# step.
# ---------------------------------------------------------------------------
	
	
class ParameterList:
	def __init__(self, parameterString):
		self.parameters = self.parseParameters(parameterString)
		self.options = []
		self.optionMap = {}
		i = 0
		for p in self.parameters:
			if p.__class__ == list:
				self.options.append(p)
				self.optionMap[i] = p 
			i += 1
	def __getitem__(self, index):
		for p in self.parameters:
			if p.__class__ == Parameter:
				if index == 0:
					return p
				else:
					index -= 1
		return [][1]
	def __len__(self):
		length = 0
		for p in self.parameters:
			if p.__class__ == Parameter:
				length += 1
		return length
	def __repr__(self):
		rep = ''
		for p in self:
			rep = rep+repr(p)+', '
		return rep[:-2]
	def expandOption(x):
		option = self.optionMap.values()[x]
		place = self.optionMap.keys()[x]
		para = self.parameters
		self.parameters = para[:place].extend(option+para[place+1:])
	def parseParameters(self, pString):
		def word(s, w):
			if not s:
				return s, w
			if s[0] == ',':
				return s[2:], w
			elif s[0] == ']':
				return s, w
			else:
				return word(s[1:], w+s[0])
		def parse(s, l):
			if not s: 
				return s, l
			car = s[0]
			if car == '[':
				sl = parse(s[1:], [])
				l.append(sl[1])
				return parse(sl[0], l)
			elif car == ']':
				return s[1:], l
			else:
				sw = word(s, '')
				l.append(translator.parameter(sw[1]))
				return parse(sw[0], l)
		return parse(pString, [])[1]

class Opcode:
	def __init__(self, parameters, outputID):
		parameters = parameters.split('\t')
		self.outputs = ParameterList(parameters[0])
		for o in self.outputs:
			o.field = str(outputID[0])
			outputID[0] += 1
		self.name = parameters[1]
		self.parameters = ParameterList(parameters[2])
	def __repr__(self):
		rep = ''
		for o in self.outputs:
			rep += o.rate+o.field
		rep += '\t'+self.name+'\t'
		for p in self.parameters:
			if p.isOpen():
				rep += str(omn.random()*p.range+p.offset)
			else:
				rep += str(p.field)
			rep += ", "
		rep = rep[:-2]
		return rep+'\n'
	def setParameter(self, index, value):
		self.parameters[index] = value
	def parameters(self, plist):
		params = []
		for i in range(len(self.parameters)):
			if plist[i] == i:
				params.append(self.parameters[i])
		return params
	def openParameters(self):
		openp = []
		for p in self.parameters:
			if p.isOpen():
				openp.append(p)
		return openp
	def nameParameters(self):
		names = []
		for p in self.parameters:
			if not p.isOpen() and p[0] != 'p':
				names.append(i)
		return names
	def pfieldParameters(self):
		pfields = []
		for p in self.parameters:
			if p[0] == 'p':
				pfields.append(i)
		return pfields

		
class OpcodeFactory:
	def opcode(self, code, out):
		if code == 'oscil':
			out[0] += 1
			return Opcode("ar\toscil\txamp, xfreq, ifnc, [iphs]", out)
		elif code == 'line':
			out[0] += 1
			return Opcode("ar\tline\tia, idur1, ib", out)
		elif code == 'out':
			return Opcode("\touts\taright, aleft", out)
		else:
			return 'do not recognize '+code

opcodes = OpcodeFactory()

class Instrument:
	def __init__(self, number):
		self.number = number
		self.names = {"out":opcodes.opcode('out')}
		self.pfields = 3
		self.outputLimit = [0]
	def __repr__(self):
		repr = "\tinstr\t"+str(self.number)+"\n"
		for n in self.names:
			repr += n
		return repr
	def addName(self, name, line):
		self.names[name] = opcodes.opcode(name, self.outputLimit)
	def getNames(self):
		self.names.keys()
	def getUnusedPfield(self):
		self.pfields += 1
		return "p"+str(self.pfields)
