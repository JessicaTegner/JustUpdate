import os
import logging
from justfuckingupdate import __version__

from justfuckingupdate.core.base import prompt
from justfuckingupdate.core.executor import CommandType, CommandExecutor
from justfuckingupdate.core.config import Config

def _cmd_version(args, extra=None):
	logging.info(f"JustFuckingUpdate version {__version__}.")

def _cmd_init(args, extra=None):
	if os.path.isfile("config.jfu"):
		logging.warning("A JustFuckingUpdate repository already exists at this location.")
		return True
	
	# setup a new repo.
	app_name = prompt("Application Name:", "MyAwezomeApp")
	app_author = prompt("Application Author:", "MyAwesomeCompany")
	update_url = prompt("Url to ping for updates:")
	logging.info("Creating config.")
	c = Config()
	c.set("app_name", app_name)
	c.set("app_author", app_author)
	c.set("update_url", update_url)
	c.save("config.jfu")
	logging.info("Saving config.")
	logging.info("Initialization done.")


def _cmd_build(args, extra=None):
	cmd = ["pyinstaller"] + extra
	executor = CommandExecutor()
	result = executor.execute(cmd, CommandType.PYINSTALLER)
	if result > 0: # error
		logging.error("Please correct the errors above and try again.")
	return True

def _cmd_make_spec(args, extra=None):
	cmd = ["pyi-makespec"] + extra
	executor = CommandExecutor()
	result = executor.execute(cmd, CommandType.PYINSTALLER)
	if result > 0: # error
		logging.error("Please correct the errors above and try again.")
	return True
