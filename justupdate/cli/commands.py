import os
import shutil
import logging
from justupdate import __version__

from justupdate.core.base import JustUpdateConstants, prompt, confirmation, get_platform_name_short
from justupdate.core.executor import CommandType, CommandExecutor
from justupdate.core.config import Config

from justupdate.repo.version import Version

def _cmd_version(args, extra=None):
	logging.info(f"JustUpdate version {__version__}.")

def _cmd_init(args, extra=None):
	if os.path.isfile(os.path.join(JustUpdateConstants.REPO_FOLDER, "config.ju")) or os.path.isdir(JustUpdateConstants.REPO_FOLDER):
		logging.warning("A JustUpdate repository already exists at this location.")
		return True
	
	# setup a new repo.
	app_name = prompt("Application Name:", "MyAwezomeApp")
	app_author = prompt("Application Author:", "MyAwesomeCompany")
	update_url = prompt("Url to ping for updates:")
	
	logging.info("Creating folder structure.")
	os.makedirs(JustUpdateConstants.REPO_FOLDER)
	logging.info("Creating config.")
	c = Config()
	c.set("app_name", app_name)
	c.set("app_author", app_author)
	c.set("update_url", update_url)
	c.save(os.path.join(JustUpdateConstants.REPO_FOLDER, "config.ju"))
	logging.info("Saving config.")
	# Copy templates from module folder to repo folder.
	logging.info("Copying templates.")
	os.makedirs(os.path.join(JustUpdateConstants.REPO_FOLDER, "templates"))
	# First, the NSIS installer template
	f = open(os.path.join(JustUpdateConstants.MODULE_FOLDER, "templates", "template.nsi"))
	nsis_template = f.read()
	f.close()
	f = open(os.path.join(JustUpdateConstants.REPO_FOLDER, "templates", "template.nsis"), "w")
	f.write(nsis_template)
	f.close()
	logging.info("Templates copied.")
	logging.info("Initialization done.")

def _cmd_clean(args, extra=None):
	if os.path.isdir(JustUpdateConstants.REPO_FOLDER) == False:
		logging.warning("No JustUpdate repository exists at this location.")
		return True
	
	# Make sure that the user really wants do delete the repository.
	confirm = confirmation("This will delete the current JustUpdate repository. Are you really sure you want to continue? ", "n")
	if confirm == False:
		logging.info("cancelled...")
		return True
	
	if confirm:
		logging.info("Cleaning repository.")
		logging.info("Deleting files.")
		shutil.rmtree(JustUpdateConstants.REPO_FOLDER)
		logging.info("Clean done.")
		return True

def _cmd_build(args, extra=None):
	try:
		shutil.rmtree(os.path.join(JustUpdateConstants.REPO_FOLDER, "work"))
	except FileNotFoundError:
		pass # It's ok if the folder doesn't exist.
	cmd = ["pyinstaller", "--distpath", os.path.join(JustUpdateConstants.REPO_FOLDER, "dist"), "--workpath", os.path.join(JustUpdateConstants.REPO_FOLDER, "work"), "-y"] + extra
	executor = CommandExecutor()
	logging.info("Building.")
	result = executor.execute(cmd, CommandType.PYINSTALLER, suppress_stdout=True, suppress_stderr=True)
	if result > 0: # error
		logging.error("Please correct the errors above and try again.")
	return True

def _cmd_commit(args, extra=None):
	"""Notes:
	1. Done - Look to see if a build is there.
	2. Assemple it into a NSIS exe on windows or pkg on mac.
	3. Calculate checksum.
	4. todo: Make repo files (versions.json or something).
	5. Move new executable to new folder.
	"""
	if os.path.isdir(os.path.join(JustUpdateConstants.REPO_FOLDER, "dist", get_platform_name_short())) == False:
		logging.error("No build for this platform found. please run \"justupdate build\".")
		return True
	if not os.listdir(os.path.join(JustUpdateConstants.REPO_FOLDER, "dist", get_platform_name_short())):
		logging.error("The build folder is empty. Please produce a new build with \"justupdate build\".")
		return True
		
	return True

def _cmd_make_spec(args, extra=None):
	cmd = ["pyi-makespec", "--name", get_platform_name_short()] + extra
	executor = CommandExecutor()
	result = executor.execute(cmd, CommandType.PYINSTALLER, suppress_stdout=True, suppress_stderr=True)
	if result > 0: # error
		logging.error("Please correct the errors above and try again.")
	else:
		logging.info("Spec file written.")
	return True
