import logging
import subprocess
from justfuckingupdate.core.base import is_windows, is_mac

class CommandType():
	"""The type of command, that the command executor should execute"""
	PYINSTALLER = 1
	EXECUTE_UPDATE_FILE = 2

class CommandExecutor():
	"""This class is responsible for the platform specific implementation of executing commands"""
	
	def execute(self, arg, type):
		if type == CommandType.PYINSTALLER:
			return self._run_platform_agnostic_command(arg)
		if type == CommandType.EXECUTE_UPDATE_FILE:
			# os specific.
			pass

	def _run_platform_agnostic_command(self, cmd):
		logging.debug("Executing command {}".format(" ".join(cmd)))
		return subprocess.call(cmd, stdout=subprocess.PIPE)


