class ChirpConfig:
	def __init__(self):
		self._config = ConfigParser.ConfigParser()
		self._config.read(os.path.expanduser('~/.chirprc'))

	def GetUsername(self):
		return self._GetOption('username')

	def GetPassword(self):
		return self._GetOption('password')

	def _GetOption(self, option):
		try:
			return self._config.get('Chirp', option)
		except:
			return None			