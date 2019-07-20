import json

class Config():
	def __init__(self):
		self._config_set = {}

	def load(self, filename):
		self._config_set = json.load(open(filename))
		return self

	def save(self, filename):
		json.dump(self._config_set, open(filename, "w"), sort_keys=True, indent="\t")
		return self

	def get(self, key):
		return self._config_set[key]

	def set(self, key, value):
		self._config_set[key] = value
		return self
