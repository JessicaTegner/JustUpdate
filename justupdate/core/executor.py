import logging
import os
import subprocess

from justupdate.core.base import get_platform_name_short

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
			cmd = getattr(self, f"_execute_update_{get_platform_name_short()}")
			return cmd(*arg)

	def _run_platform_agnostic_command(self, cmd, stdin):
		logging.debug("Executing command {}".format(" ".join(cmd)))
		result = subprocess.run(cmd, input=stdin, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, universal_newlines=True)
		return result.returncode, result.stdout

	def _execute_update_win(self, folder, app_name, version):
		return subprocess.Popen(["powershell.exe", "Start-Process", os.path.join(folder, app_name+"-"+version+".exe"), "-Verb", "runAs"])

	def _execute_update_mac(self, folder, app_name, version):
		path = os.path.join(folder, app_name+"-"+version+".pkg")
		return subprocess.call(f"osascript -e 'do shell script \"installer -pkg \\\"{path}\\\" -target /\" with prompt \"{app_name} WANTS TO make changes\" with administrator privileges'", shell=True) == 0
