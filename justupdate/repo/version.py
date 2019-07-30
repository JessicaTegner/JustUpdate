class Version():
	"""This class converts the JFU version numbers to and from strings"""
	def __init__(self, version):
		self.is_stable = False
		self.is_beta = False
		self.is_alpha = False
		self.raw_version = self.from_string(version)
	
	def to_nsis_compliant(self):
		if len(self.raw_version) == 5:
			return "{0}.{1}.{2}.{4}".format(*self.raw_version)
		if len(self.raw_version) == 4:
			return "{0}.{1}.{2}.{3}".format(*self.raw_version)
		if len(self.raw_version) == 3:
			return "{0}.{1}.{2}.0".format(*self.raw_version)
	
	def to_mac_compliant(self):
			return "{0}.{1}.{2}".format(*self.raw_version)
		
	
	def to_string(self):
		if len(self.raw_version) == 5:
			return "{0}.{1}.{2}a{4}".format(*self.raw_version)
		if len(self.raw_version) == 4:
			return "{0}.{1}.{2}b{3}".format(*self.raw_version)
		if len(self.raw_version) == 3:
			return "{0}.{1}.{2}".format(*self.raw_version)
	
	def from_string(self, version):
		tmp_version = version.replace("alpha", ".0.").replace("beta", ".").replace("a", ".0.").replace("b", ".").split(".")
		if len(tmp_version) < 3:
			raise ValueError("""Invalid version string supplied. Valid versions are (examples):\n"1.0.0"\n"1.0.0a1"\n"1.0.0b1"\n"1.0.0alpha1"\n"1.0.0beta1" """)
		if len(tmp_version) == 5:
			self.is_alpha = True
		if len(tmp_version) == 4:
			self.is_beta = True
		if len(tmp_version) == 3:
			self.is_stable = True
		return tmp_version
	
	def to_human_readable(self):
		if len(self.raw_version) == 5:
			return "{0}.{1}.{2} alpha {4}".format(*self.raw_version)
		if len(self.raw_version) == 4:
			return "{0}.{1}.{2} beta {3}".format(*self.raw_version)
		if len(self.raw_version) == 3:
			return "{0}.{1}.{2}".format(*self.raw_version)
	
	def _converted_raw_version(self):
		return list(map(int, self.raw_version))
	
	def __eq__(self, other):
		return self._converted_raw_version() == other._converted_raw_version()
	
	def __ne__(self, other):
		return self._converted_raw_version() != other._converted_raw_version()
	
	def __gt__(self, other):
		return self._converted_raw_version() > other._converted_raw_version()
	
	def __lt__(self, other):
		return self._converted_raw_version() < other._converted_raw_version()

