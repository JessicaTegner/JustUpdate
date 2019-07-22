import os
import logging
import shutil

from justupdate.core import data_manager
from justupdate.core.base import JustUpdateConstants, get_platform_name_short
from justupdate.core.config import Config
from justupdate.core.executor import CommandExecutor, CommandType

from justupdate.repo import template
from justupdate.repo.version import Version
from justupdate.repo.metadata import MetaData, MetaDataChannel

class Committer():
	def __init__(self, version):
		self.config = Config()
		self.config.load(os.path.join(JustUpdateConstants.REPO_FOLDER, "config.ju"))
		self.version = Version(version)
		self.executor = CommandExecutor()
	
	def insure_build_availability(self):
		if os.path.isdir(os.path.join(JustUpdateConstants.REPO_FOLDER, "dist", get_platform_name_short())) == False:
			return False
		if not os.listdir(os.path.join(JustUpdateConstants.REPO_FOLDER, "dist", get_platform_name_short())):
			return False
		return True
	
	def setup(self):
		if os.path.isdir(os.path.join(JustUpdateConstants.REPO_FOLDER, "new")) == False:
			os.makedirs(os.path.join(JustUpdateConstants.REPO_FOLDER, "new"))
		if os.path.isdir(os.path.join(JustUpdateConstants.REPO_FOLDER, "deploy")) == False:
			os.makedirs(os.path.join(JustUpdateConstants.REPO_FOLDER, "deploy"))
	
	def produce_executable(self):
		cmd = getattr(self, f"_produce_executable_{get_platform_name_short()}")
		return cmd()
	
	def create_metadata(self):
		cmd = getattr(self, f"_create_metadata_{get_platform_name_short()}")
		return cmd()
	
	def finalize(self):
		cmd = getattr(self, f"_finalize_{get_platform_name_short()}")
		return cmd()
	
	def _produce_executable_win(self):
		tmp = template.prepare_template(self.version)
		cmd = ["makensis", "/V1", "-"]
		result, stdout = self.executor.execute(cmd, CommandType.RAW, stdin=tmp)
		if result != 0:
			print(stdout)
			logging.error("Please correct the errors above and try again.")
			return False
		return True
	
	def _produce_executable_mac(self):
		pass
	
	def _create_metadata_win(self):
		logging.info("Calculating checksum.")
		checksum = data_manager.calculate_checksum(os.path.join(JustUpdateConstants.REPO_FOLDER, "new", "{0}-{1}.exe".format(self.config.get("app_name"), self.version.to_string())))
		logging.info("Looking for existing metadata.")
		md = MetaData(get_platform_name_short())
		md.add_metadata("{0}-{1}.exe".format(self.config.get("app_name"), self.version.to_string()), checksum, self.version.to_string())
		logging.info("Saving updated metadata.")
		md.save() # The updated metadata is saved to "ju-repo/deploy/metadata.ju".
		return True
	
	def _create_metadata_mac(self):
		pass
	
	def _finalize_win(self):
		logging.info("Moving executable.")
		shutil.move(os.path.join(JustUpdateConstants.REPO_FOLDER, "new", "{0}-{1}.exe".format(self.config.get("app_name"), self.version.to_string())), os.path.join(JustUpdateConstants.REPO_FOLDER, "deploy"))
		#cleanup ju-repo/dist/win
		shutil.rmtree(os.path.join(JustUpdateConstants.REPO_FOLDER, "dist", "win"))
	
	def _finalize_mac(self):
		pass

