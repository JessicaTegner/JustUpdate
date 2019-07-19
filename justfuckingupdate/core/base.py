import platform

def is_windows():
	return platform.System() == "Windows"

def is_mac():
	return platform.System() == "Darwin"

