import os
import logging
from justfuckingupdate import __version__

from justfuckingupdate.core.executor import CommandType, CommandExecutor

def _cmd_version(args, extra=None):
	logging.info(f"JustFuckingUpdate version {__version__}.")

def _cmd_build(args, extra=None):
	print(args)
	print(extra)
	return True

def _cmd_make_spec(args, extra=None):
	cmd = ["pyi-makespec"] + extra
	executor = CommandExecutor()
	result = executor.execute(cmd, CommandType.PYINSTALLER)
	if result > 0: # error
		logging.error("Please correct the errors above and try again.")
	return True
