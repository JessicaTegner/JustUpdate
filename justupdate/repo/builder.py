import shutil
import logging
import os

from justupdate.core.base import JustUpdateConstants, get_platform_name_short
from justupdate.core.config import Config
from justupdate.core.executor import CommandExecutor, CommandType

class Builder():
	def clean(self):
		try:
			shutil.rmtree(os.path.join(JustUpdateConstants.REPO_FOLDER, "work"))
		except FileNotFoundError:
			pass # It's ok if the folder doesn't exist.
	
	def build(self, args, extra_args):
		cmd = ["pyinstaller", "--distpath", os.path.join(JustUpdateConstants.REPO_FOLDER, "dist"), "--workpath", os.path.join(JustUpdateConstants.REPO_FOLDER, "work"), "-y", args] + extra_args
		executor = CommandExecutor()
		logging.info("Building.")
		result, stdout = executor.execute(cmd, CommandType.RAW)
		if result > 0: # error
			print(stdout)
			logging.error("Please correct the errors above and try again.")
		else:
			logging.info("Build completed.")
		return result == 0
	
	def post_build(self):
		cmd = getattr(self, f"_post_build_{get_platform_name_short()}")
		return cmd()
	
	def _post_build_win(self):
		logging.info("Checking build integrity")
		if os.path.isdir(os.path.join(JustUpdateConstants.REPO_FOLDER, "dist", "win")) == False:
			logging.error("Unable to find the build fonder.")
		config = Config()
		config.load(os.path.join(JustUpdateConstants.REPO_FOLDER, "config.ju"))
		app_name = config.get("app_name")
		# First look for .exe.manifest, and rename that if it exists.
		try:
			os.rename(os.path.join(JustUpdateConstants.REPO_FOLDER, "dist", "win", "win.exe.manifest"), os.path.join(JustUpdateConstants.REPO_FOLDER, "dist", "win", f"{app_name}.exe.manifest"))
		except:
			pass
		# then try for the exe itself.
		try:
			os.rename(os.path.join(JustUpdateConstants.REPO_FOLDER, "dist", "win", "win.exe"), os.path.join(JustUpdateConstants.REPO_FOLDER, "dist", "win", f"{app_name}.exe"))
		except:
			raise
		logging.info("Done")
	
	def _post_build_mac(self):
		pass
