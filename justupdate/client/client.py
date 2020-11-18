import hashlib
import json
import os
import shutil
import threading

import requests
import requests_cache
try:
	from urlparse import urljoin
except:
	from urllib.parse import urljoin

from appdirs import user_data_dir

from justupdate.core import data_manager
from justupdate.core.base import get_platform_name_short
from justupdate.core.executor import CommandExecutor, CommandType

from justupdate.repo.metadata import MetaData, MetaDataChannel
from justupdate.repo.version import Version

from justupdate.client.exceptions import InvalidUpdateChannelException, ChecksumValidationError

class JustUpdateClient():
	"""The main client module. You'll want to call this in your code, to check for updates to your application"""
	def __init__(self, config, current_version, channel, callback=None):
		"""Expected parameters
		This constructor expects a class with the following parameters (at minimum):
		
		app_name (str) : The application name.
		app_author (str) : The application author.
		update_url (str) : The url where the metadata and updates are stored.
		cache_timeout (int) : The time in seconds, before metadata will be downloaded from the server, if present in cache.
		
		In addition:
		current_version (str) : The applications current version.
		channel (str) : The channel which for look for updates on (either alpha, beta or stable).
		callback (callable, optional) a function to call on downlaod progress.
		"""
		self._client_config = config
		self.app_name = config.app_name
		self.app_author = config.app_author
		self.update_url = config.update_url
		self.current_version = current_version
		self.channel = channel
		self.callbacks = []
		if callback is not None:
			self.add_callback(callback)
		self._user_data_dir = os.path.join(user_data_dir(self.app_name, self.app_author), "updates")
		self._update_version = None
		self._metadata = None
		self._is_downloaded = False
		self._is_post_update = False
		if os.path.exists(os.path.join(self._user_data_dir, ".postupdate")):
			self._is_post_update = True
	
	def add_callback(self, callback):
		if callable(callback) == False:
			raise ValueError("\"Callback\" most be callable.")
		self.callbacks.append(callback)
	
	def is_downloaded(self):
		return self._is_downloaded
	
	def is_post_update(self):
		return self._is_post_update
	
	def post_update_cleanup(self):
		if os.path.exists(os.path.join(self._user_data_dir, ".postupdate")) == False:
			return
		os.remove(os.path.join(self._user_data_dir, ".postupdate"))
	
	def cleanup(self):
		try:
			shutil.rmtree(self._user_data_dir)
			return True
		except OSError:
			return True
		except:
			raise
			return False
		
	def update_available(self, bypass_metadata_cache=False):
		"""Checks for updates to the application
		
		args:
			bypass_metadata_cache (bool) : Bypass the available cache for the metadata, True to force redownload of metadata, False to use cache. (Default False).
		"""
		if self.channel not in ("stable", "beta", "alpha"):
			raise InvalidUpdateChannelException(f"\"{channel} is an invalid update channel. Available channels are alpha, beta and stable.")
		current_version = Version(self.current_version)
		try:
			self._metadata = self._load_metadata(bypass_metadata_cache)
		except requests.exceptions.HTTPError as e:
			raise e
			return False
		if self.channel == "alpha":
			newest_version = self._metadata.get_newest(MetaDataChannel.ALPHA)
			if newest_version is None:
				return False
			if newest_version > current_version:
				self._update_version = newest_version
				return True
			else:
				return False
		if self.channel == "beta":
			newest_version = self._metadata.get_newest(MetaDataChannel.BETA)
			if newest_version == None:
				return False
			if newest_version > current_version:
				self._update_version = newest_version
				return True
			else:
				return False
		if self.channel == "stable":
			newest_version = self._metadata.get_newest(MetaDataChannel.STABLE)
			if newest_version is None:
				return False
			if newest_version > current_version:
				self._update_version = newest_version
				return True
			else:
				return False
	
	def download_update(self, background=False):
		if self._metadata is None:
			self._metadata = self._load_metadata()
		new_version = ""
		if self._update_version is None:
			if self.channel == "alpha":
				new_version = self._metadata.get_newest(MetaDataChannel.ALPHA).to_string()
			if self.channel == "beta":
				new_version = self._metadata.get_newest(MetaDataChannel.BETA).to_string()
			if self.channel == "stable":
				new_version = self._metadata.get_newest(MetaDataChannel.STABLE).to_string()
		else:
			new_version = self._update_version.to_string()
		if background:
			thread = threading.Thread(target=self._download_update, args=(new_version,))
			thread.start()
			return
		else:
			self._download_update(new_version)
	
	def execute_update(self):
		f = open(os.path.join(self._user_data_dir, ".postupdate"), "w")
		f.close()
		executor = CommandExecutor()
		return executor.execute((self._user_data_dir, self.app_name, self._update_version.to_string()), CommandType.EXECUTE_UPDATE_FILE)
	
	def _load_metadata(self, bypass_metadata_cache_cache):
		md = ""
		try:
			md = self._download_metadata(f"metadata-{get_platform_name_short()}.ju", bypass_metadata_cache_cache)
		except requests.ConnectTimeout:
			return None
		except:
			raise
		md = data_manager.decompress(md)
		md = json.loads(md)
		metadata = MetaData()
		metadata.apply_metadata(md)
		return metadata
	
	def _download_update(self, new_version):
		metadata = self._metadata.get_metadata_for_version(new_version)
		self._download_file(metadata["filename"], metadata["checksum"], True)
		self._is_downloaded = True
	
	def _download_metadata(self, file, bypass_metadata_cache=False):
		if os.path.isdir(self._user_data_dir) == False:
			os.makedirs(self._user_data_dir)
		url = urljoin(self.update_url, file)
		timeout = getattr(self._client_config, "cache_timeout", 1)
		s = requests_cache.CachedSession(cache_name= os.path.join(self._user_data_dir, "cache"), expire_after=timeout, old_data_on_error=True)
		response = None
		if bypass_metadata_cache:
			with s.cache_disabled():
				response = s.get(url)
		else:
			response = s.get(url)
		return response.content
	
	def _download_file(self, file, checksum=None, do_callbacks=False):
		if os.path.isdir(self._user_data_dir) == False:
			os.makedirs(self._user_data_dir)
		url = urljoin(self.update_url, file)
		local_filename = os.path.join(self._user_data_dir, url.split('/')[-1])
		downloaded_checksum = hashlib.sha512()
		with requests.get(url, stream=True) as r:
			r.raise_for_status()
			with open(local_filename, 'wb') as f:
				for chunk in r.iter_content(chunk_size=1024*1024): 
					if chunk: # filter out keep-alive new chunks
						f.write(chunk)
						total = int(r.headers.get('content-length', 0))
						current = os.fstat(f.fileno()).st_size
						status = {"total": total, "percentage": round(current/total*100, 0), "item": file}
						downloaded_checksum.update(chunk)
						if do_callbacks:
							for callback in self.callbacks:
								callback(status)
		if checksum is not None:
			if checksum != downloaded_checksum.hexdigest():
				raise ChecksumValidationError(file)
		return local_filename
