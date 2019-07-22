import os
import logging
import subprocess
from justupdate.core.base import is_windows, is_mac

class CommandType():
	"""The type of command, that the command executor should execute"""
	RAW = 1
	CHECK = 2
	EXECUTE_UPDATE_FILE = 3

class CommandExecutor():
	"""This class is responsible for the platform specific implementation of executing commands"""
	
	def execute(self, arg, type, stdin=None):
		if type == CommandType.RAW:
			return self._run_platform_agnostic_command(arg, stdin)
		if type == CommandType.CHECK:
			try:
				result, stdout = self._run_platform_agnostic_command(arg, stdin)
				return True if result == 0 else False
			except FileNotFoundError:
				return False
		if type == CommandType.EXECUTE_UPDATE_FILE:
			# os specific.
			pass

	def _run_platform_agnostic_command(self, cmd, stdin):
		logging.debug("Executing command {}".format(" ".join(cmd)))
		result = subprocess.run(cmd, input=stdin, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, universal_newlines=True)
		return result.returncode, result.stdout


