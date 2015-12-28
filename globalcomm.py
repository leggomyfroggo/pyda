class __GlobalComm__:
	def __init__(self):
		self.states = {}
	
	def SetState(self, Key, Value):
		self.states[Key] = Value
		return Value

	def GetState(self, Key):
		return self.states.get(Key)

GlobalComm = __GlobalComm__()