"""these tests, test the "justupdate.client" module"""
from . import util

from justupdate.client.client import JustUpdateClient

class DummyClientConfig():
	app_name = "DummyApp"
	app_author = "DummyCompany"
	update_url = "https://dummycompany.com/dummyapp"
version = "1.2.3a4"
channel = "alpha"


def test_client_initalization():
	client = JustUpdateClient(DummyClientConfig(), version, channel)
	assert client.app_name == DummyClientConfig.app_name
	assert client.app_author == DummyClientConfig.app_author
	assert client.update_url == DummyClientConfig.update_url

def test_client_initalization_with_callback():
	def dummy_callback(status):
		print(str(status))
	
	client = JustUpdateClient(DummyClientConfig(), version, channel, dummy_callback)
	assert len(client.callbacks) == 1

def test_post_update():
	client = JustUpdateClient(DummyClientConfig(), version, channel)
	assert client.is_post_update() == False
	client._is_post_update = True # for testing only
	assert client.is_post_update()

def test_cleanup():
	client = JustUpdateClient(DummyClientConfig(), version, channel)
	assert client.cleanup() == True

