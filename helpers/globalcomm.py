class __GlobalComm:
	"""
	A class used for communicating game information globally between objects.
	"""
	def __init__(self):
		"""
		Initializes the GlobalComm.
		"""
		self.states = {}
	
	def SetState(self, Key, Value):
		"""
		Sets a global state for use by other objects.

		Args:
			Key:	The key to associate with the value being stored.
			Value:	The object to set.
		"""
		self.states[Key] = Value
		return Value

	def GetState(self, Key):
		"""
		Gets a global state that has been previously set.

		Args:
			Key:	The key associated with the desired object.

		Returns:
			The object associated with the given key.
		"""
		return self.states.get(Key)

GlobalComm = __GlobalComm()