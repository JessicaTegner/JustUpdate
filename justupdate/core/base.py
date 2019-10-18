import os
import logging
import platform
import justupdate

# Miss variables and functions.
class JustUpdateConstants():
	REPO_FOLDER = "ju-repo"
	MODULE_FOLDER = os.path.dirname(os.path.abspath(justupdate.__file__))

def is_windows():
	return platform.system() == "Windows"

def is_mac():
	return platform.system() == "Darwin"

def get_platform_name_short():
	if is_windows():
		return "win"
	if is_mac():
		return "mac"

def prompt(question, default="", allow_empty=False):
	while True:
		logging.info(question + " {}".format("Default {}:".format(default) if default != "" else "No default available:"))
		result = input(">> ") or default
		if result == "" and allow_empty==False:
			logging.warning("This value cannot be left blank.")
			continue
		correction = input("You entered {}, is that correct? n/y".format(result)) or "n"
		if correction == "y":
			return result

def confirmation(question, default):
	while True:
		logging.info(question + " y / n, default {}:".format(default))
		result = input(">> ") or default
		if result == "":
			logging.warning("Please either enter \"y\" or \"n\".")
			continue
		if result == "y":
			return True
		if result == "n":
			return False
		else:
			logging.warning("Invalid value \"{}\". Please either enter \"y\" or \"n\".".format(result))
