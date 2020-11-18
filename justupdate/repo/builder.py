import io
import logging
import os
import shutil

from justupdate.core.base import get_platform_name_short
from justupdate.core.base import JustUpdateConstants
from justupdate.core.config import Config
from justupdate.core.executor import CommandExecutor
from justupdate.core.executor import CommandType

class Builder():
	def __init__(self):
		self.config = Config()
		self.config.load(os.path.join(JustUpdateConstants.REPO_FOLDER, "config.ju"))
	
	def clean(self):
		try:
			shutil.rmtree(os.path.join(JustUpdateConstants.REPO_FOLDER, "work"))
		except FileNotFoundError:
			pass # It's ok if the folder doesn't exist.
		cmd = getattr(self, f"_clean_{get_platform_name_short()}")
		return cmd()
	
	def _clean_win(self):
		try:
			shutil.rmtree(os.path.join(JustUpdateConstants.REPO_FOLDER, "dist", "win"))
		except FileNotFoundError:
			pass # It's ok if the folder doesn't exist.
	
	def _clean_mac(self):
		try:
			shutil.rmtree(os.path.join(os.getcwd(), JustUpdateConstants.REPO_FOLDER, "dist", "mac"))
		except FileNotFoundError:
			pass # It's ok if the folder doesn't exist.
		try:
			shutil.rmtree(os.path.join(os.getcwd(), JustUpdateConstants.REPO_FOLDER, "dist", "{}.app".format(self.config.get("app_name"))))
		except FileNotFoundError:
			pass # It's ok if the folder doesn't exist.
		try:
			os.remove(os.path.join(os.getcwd(), JustUpdateConstants.REPO_FOLDER, "dist", "mac"))
		except FileNotFoundError:
			pass # It's ok if the folder doesn't exist.
	
	def build(self, args, extra_args):
		cmd = ["pyinstaller", "--distpath", os.path.join(os.getcwd(), JustUpdateConstants.REPO_FOLDER, "dist"), "--workpath", os.path.join(os.getcwd(), JustUpdateConstants.REPO_FOLDER, "work"), "-y", args] + extra_args
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
		app_name = self.config.get("app_name")
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
		if os.path.isfile(os.path.join(JustUpdateConstants.REPO_FOLDER, "dist", "mac")): # asume unix executable.
			raise ValueError("--onefile is not supported at the moment. For now the only mode supported are --onedir --windowed (creating an application bundle)")
			return
		if os.path.isdir(os.path.join(JustUpdateConstants.REPO_FOLDER, "dist", "mac.app")): # asume mac application bundle.
			os.rename(os.path.join(JustUpdateConstants.REPO_FOLDER, "dist", "mac.app", "Contents", "MacOS", "mac"), os.path.join(JustUpdateConstants.REPO_FOLDER, "dist", "mac.app", "Contents", "MacOS", self.config.get("app_name")))
			os.rename(os.path.join(JustUpdateConstants.REPO_FOLDER, "dist", "mac.app"), os.path.join(JustUpdateConstants.REPO_FOLDER, "dist", "{}.app".format(self.config.get("app_name"))))
			# also temporary update the plist file (note it will be overwritten in commit, only reason to do this, is so the end developer can test the app before commiting).
			with open(os.path.join(JustUpdateConstants.REPO_FOLDER, "dist", "{}.app".format(self.config.get("app_name")), "Contents", "Info.plist"), encoding="utf-8") as f:
				plist_data = f.readlines()
			new_plist_data = []
			for d in plist_data:
				if "mac" in d:
					new_plist_data.append(d.replace("mac", self.config.get("app_name")))
				else:
					new_plist_data.append(d)
			with open(os.path.join(JustUpdateConstants.REPO_FOLDER, "dist", "{}.app".format(self.config.get("app_name")), "Contents", "Info.plist"), "w", encoding="utf-8") as f:
				for d in new_plist_data:
					f.write(d)
