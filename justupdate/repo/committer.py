import logging
import os
import shutil

from justupdate.core import data_manager
from justupdate.core.base import get_platform_name_short
from justupdate.core.base import JustUpdateConstants
from justupdate.core.config import Config
from justupdate.core.executor import CommandExecutor
from justupdate.core.executor import CommandType
from justupdate.repo import template
from justupdate.repo.metadata import MetaData
from justupdate.repo.metadata import MetaDataChannel
from justupdate.repo.version import Version

class Committer():
	def __init__(self, version):
		self.config = Config()
		self.config.load(os.path.join(JustUpdateConstants.REPO_FOLDER, "config.ju"))
		self.version = Version(version)
		self.executor = CommandExecutor()
	
	def setup(self):
		if os.path.isdir(os.path.join(JustUpdateConstants.REPO_FOLDER, "new")) == False:
			os.makedirs(os.path.join(JustUpdateConstants.REPO_FOLDER, "new"))
		if os.path.isdir(os.path.join(JustUpdateConstants.REPO_FOLDER, "deploy")) == False:
			os.makedirs(os.path.join(JustUpdateConstants.REPO_FOLDER, "deploy"))
	
	def insure_build_availability(self):
		cmd = getattr(self, f"_insure_build_availability_{get_platform_name_short()}")
		return cmd()
	
	def produce_executable(self):
		cmd = getattr(self, f"_produce_executable_{get_platform_name_short()}")
		return cmd()
	
	def create_metadata(self):
		cmd = getattr(self, f"_create_metadata_{get_platform_name_short()}")
		return cmd()
	
	def finalize(self):
		cmd = getattr(self, f"_finalize_{get_platform_name_short()}")
		return cmd()
	
	def _insure_build_availability_win(self):
		if os.path.isdir(os.path.join(JustUpdateConstants.REPO_FOLDER, "dist", "win")) == False:
			return False
		if not os.listdir(os.path.join(JustUpdateConstants.REPO_FOLDER, "dist", "win")):
			return False
		return True
	
	def _insure_build_availability_mac(self):
		if not os.path.isdir(os.path.join(JustUpdateConstants.REPO_FOLDER, "dist", "{}.app".format(self.config.get("app_name")))):
			return False
		return True
	
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
		logging.debug("Updating Info.plist and installation scripts.")
		tmp = template.prepare_template(self.version)
		logging.debug("Assembling pkg installer.")
		cmd = ["productbuild", "--scripts", os.path.join(JustUpdateConstants.REPO_FOLDER, "templates", "mac", "scripts"), "--component", os.path.join(JustUpdateConstants.REPO_FOLDER, "dist", "{}.app".format(self.config.get("app_name"))), "/Applications", os.path.join(JustUpdateConstants.REPO_FOLDER, "new", "{}-{}.pkg".format(self.config.get("app_name"), self.version.to_string()))]
		result, stdout = self.executor.execute(cmd, CommandType.RAW)
		if result != 0:
			print(stdout)
			logging.error("Please correct the errors above and try again.")
			return False
		return True
	
	def _create_metadata_win(self):
		logging.info("Calculating checksum.")
		checksum = data_manager.calculate_checksum(os.path.join(JustUpdateConstants.REPO_FOLDER, "new", "{}-{}.exe".format(self.config.get("app_name"), self.version.to_string())))
		logging.info("Looking for existing metadata.")
		md = MetaData()
		md.apply_metadata(md.load())
		md.add_metadata("{}-{}.exe".format(self.config.get("app_name"), self.version.to_string()), checksum, self.version.to_string())
		logging.info("Saving updated metadata.")
		md.save() # The updated metadata is saved to "ju-repo/deploy/metadata.ju".
		return True
	
	def _create_metadata_mac(self):
		logging.info("Calculating checksum.")
		checksum = data_manager.calculate_checksum(os.path.join(JustUpdateConstants.REPO_FOLDER, "new", "{}-{}.pkg".format(self.config.get("app_name"), self.version.to_string())))
		logging.info("Looking for existing metadata.")
		md = MetaData()
		md.apply_metadata(md.load())
		md.add_metadata("{}-{}.pkg".format(self.config.get("app_name"), self.version.to_string()), checksum, self.version.to_string())
		logging.info("Saving updated metadata.")
		md.save() # The updated metadata is saved to "ju-repo/deploy/metadata.ju".
		return True
	
	def _finalize_win(self):
		logging.info("Moving executable.")
		shutil.move(os.path.join(JustUpdateConstants.REPO_FOLDER, "new", "{}-{}.exe".format(self.config.get("app_name"), self.version.to_string())), os.path.join(JustUpdateConstants.REPO_FOLDER, "deploy"))
		#cleanup ju-repo/dist/win
		shutil.rmtree(os.path.join(JustUpdateConstants.REPO_FOLDER, "dist", "win"))
	
	def _finalize_mac(self):
		logging.info("Moving executable.")
		shutil.move(os.path.join(JustUpdateConstants.REPO_FOLDER, "new", "{}-{}.pkg".format(self.config.get("app_name"), self.version.to_string())), os.path.join(JustUpdateConstants.REPO_FOLDER, "deploy"))
		#cleanup ju-repo/dist/mac
		try:
			shutil.rmtree(os.path.join(JustUpdateConstants.REPO_FOLDER, "dist", "mac"))
		except:
			pass
		try:
			shutil.rmtree(os.path.join(JustUpdateConstants.REPO_FOLDER, "dist", "{}.app".format(self.config.get("app_name"))))
		except:
			pass
