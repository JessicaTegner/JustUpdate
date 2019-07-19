import logging
import platform

# Miss variables and functions.
class JFU():
	JFU_FOLDER_NAME = "jfu"

def is_windows():
	return platform.System() == "Windows"

def is_mac():
	return platform.System() == "Darwin"

def prompt(question, default="", allow_empty=False):
	while True:
		logging.info(question + " {}".format(f"Default {default}:" if default != "" else "No default available:"))
		result = input(">> ") or default
		if result == "" and allow_empty==False:
			logging.warning("This value cannot be left blank.")
			continue
		correction = input(f"You entered {result}, is that correct? n/y") or "n"
		if correction == "y":
			return result

def confirmation(question, default):
	while True:
		logging.info(question + f" y / n, default {default}:")
		result = input(">> ") or default
		if result == "":
			logging.warning("Please either enter \"y\" or \"n\".")
			continue
		if result == "y":
			return True
		if result == "n":
			return False
		else:
			logging.warning(f"Invalid value \"result\". Please either enter \"y\" or \"n\".")

