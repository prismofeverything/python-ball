# a class to represent finite state automata.  essentially, a state contains
# a condition to be tested on a given environment and the result is the 
# production of the next state.

# the automata is used by subclassing FSCondition and overriding the test(self,
# environment) function with a conditional statement that depending on the 
# state of 'environment' returns two or more distinct FSConditions.  
# ------------------------------------------------------------------

class FSCondition:
	def __repr__(self):
		return "absolute condition"
	def test(self, environment):
		return self

# --------------------------------------------------------------------------
# FSAutomata will work with any condition that implements the test(environment)
# interface.  it is created with a condition and changes its state based on the
# value of 'environment' in the shift(environment) function call.
# ---------------------------------------------------------------

class FSAutomata:
	def __init__(self, condition):
		self.condition = condition
	def __repr__(self):
		return str(self.condition)
	def shift(self, environment):
		self.condition = self.condition.test(environment)



