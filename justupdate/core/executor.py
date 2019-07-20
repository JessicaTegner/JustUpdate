import os
import logging
import subprocess
from justupdate.core.base import is_windows, is_mac

class CommandType():
	"""The type of command, that the command executor should execute"""
	PYINSTALLER = 1
	EXECUTE_UPDATE_FILE = 2

class CommandExecutor():
	"""This class is responsible for the platform specific implementation of executing commands"""
	
	def execute(self, arg, type, suppress_stdout=True, suppress_stderr=False):
		if type == CommandType.PYINSTALLER:
			return self._run_platform_agnostic_command(arg, suppress_stdout, suppress_stderr)
		if type == CommandType.EXECUTE_UPDATE_FILE:
			# os specific.
			pass

	def _run_platform_agnostic_command(self, cmd, suppress_stdout, suppress_stderr):
		logging.debug("Executing command {}".format(" ".join(cmd)))
		with open(os.devnull, "w") as devnull:
			result = subprocess.run(cmd, stdout=devnull if suppress_stdout else None, stderr=devnull if suppress_stderr else None)
			return result.returncode


