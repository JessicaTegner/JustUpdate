import json
import logging
import os
import sys

import paramiko
from scp import SCPClient
from scp import SCPException

from justupdate.core import data_manager
from justupdate.core.base import JustUpdateConstants
from justupdate.core.base import prompt

class UploadManager():
	def __init__(self):
		self.upload_services = {}
		# register build in services.
		self.register_upload_service("gh-archive", GitHubArchiver)
		self.register_upload_service("scp", SCPUploader)
	
	def register_upload_service(self, name, service):
		if issubclass(service, UploaderBase) == False:
			raise ValueError(f"\"{service}\" most inherit from \"UploaderBase\".")
		self.upload_services[name] = service
	
	def get_upload_service(self, name):
		if name not in self.upload_services:
			return None
		return self.upload_services[name]
	
	def get_available_upload_services(self):
		return self.upload_services.keys()
	
	def get_service_description(self, name):
		if name not in self.upload_services.keys():
			raise ValueError("Invalid uploader service.")
			return
		service = self.upload_services[name]
		description = ""
		try:
			description = service.description
		except AttributeError:
			description = "No description available."
		return description
	
	def load_settings(self, name):
		if os.path.isfile(os.path.join(JustUpdateConstants.REPO_FOLDER, "credentials.ju")) == False:
			return None
		settings = data_manager.open_file_unicode(os.path.join(JustUpdateConstants.REPO_FOLDER, "credentials.ju"), "r")
		settings = json.loads(settings)
		if name not in settings:
			return None
		return settings[name]
	
	def save_settings(self, name, new_settings):
		settings = {}
		try:
			settings = data_manager.open_file_unicode(os.path.join(JustUpdateConstants.REPO_FOLDER, "credentials.ju"), "r")
			settings = json.loads(settings)
		except FileNotFoundError:
			pass
		try:
			del settings[name]
		except KeyError: # settings didn't exist to begin with
			pass
		settings[name] = new_settings
		json.dump(settings, open(os.path.join(JustUpdateConstants.REPO_FOLDER, "credentials.ju"), "w"), indent="\t")
		return new_settings

class UploaderBase():
	def connect(self, *args):
		pass
	
	def upload_file(self, local_file, *args):
		pass
	
	def disconnect(self):
		pass

class GitHubArchiver(UploaderBase):
	description = "Archive the produced builds (without uploading them to a third party server). Useful if using GitHub as the updater url."
	def __init__(self, manager):
		pass

class SCPUploader(UploaderBase):
	description = "Upload the produced builds to a third party server using the ssh protocol."
	def __init__(self, manager):
		self.manager = manager
		self.client = paramiko.SSHClient()
		self.client.load_system_host_keys()
		self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		self.connected = False
		self.settings = self.manager.load_settings("scp")
		if self.settings is None:
			self._fill_out_credentials()
		
	def connect(self, *args):
		if self.settings is None:
			self._fill_out_credentials()
			return
		if self.settings["key_file"] is not None:
			logging.info("Connecting to {}@{}:{} with ssh key from {}.".format(self.settings["username"], self.settings["host"], self.settings["port"], self.settings["key_file"]))
			self.client.connect(self.settings["host"], self.settings["port"], self.settings["username"], self.settings["password"], key_filename=self.settings["key_file"])
		else:
			logging.info("Connecting to {}@{}:{}.".format(self.settings["username"], self.settings["host"], self.settings["port"]))
			self.client.connect(self.settings["host"], self.settings["port"], self.settings["username"], self.settings["password"])
		self.scp = SCPClient(self.client.get_transport(), progress=self._progress)
		self.connected = True
		logging.info("Connected.")
	
	def upload_file(self, local_file, **args):
		if self.connected == False:
			return False
		if os.path.exists(local_file) == False:
			raise FileNotFoundError
		try:
			self.scp.put(local_file, self.settings["remote_path"], **args)
		except SCPException:
			self.disconnect()
			raise
	
	def disconnect(self):
		if self.connected:
			logging.info("Disconnecting...")
			self.client.close()
			logging.info("Disconnected.")
	
	def _progress(self, filename, size, sent):
		sys.stdout.write("{:.2f} - {} \r".format(float(sent)/float(size)*100, filename.decode()))
	
	def _fill_out_credentials(self):
		logging.info("SCPUploader credentials setup.")
		host = prompt("SCP Host: ")
		port = prompt("SCP Port: ", default=22)
		username = prompt("SCP username: ")
		password = prompt("SCP password (either for username or for ssh key): ", allow_empty=True)
		key_file = prompt("SSH Key (if applicable): ", default=None)
		remote_path = prompt("Remote path to upload to: ")
		self.settings = self.manager.save_settings("scp", {"host": host, "port": port, "username": username, "password": password, "key_file": key_file, "remote_path": remote_path})
		return self.connect()
