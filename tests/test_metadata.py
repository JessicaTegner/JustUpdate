"""This tests the metadata format"""

from . import util
from justupdate.repo.metadata import MetaData, MetaDataChannel
from justupdate.repo.version import Version

def test_metadata_initialization():
	md = MetaData()
	assert isinstance(md, MetaData)
	assert len(md._metadata) == 0

def test_metadata_with_one_version():
	md = MetaData()
	assert len(md._metadata) == 0
	md.add_metadata("test_app-1.0.0.exe", "DUMMY_CHECKSUM", "1.0.0")
	assert len(md._metadata) == 1
	result = md.get_metadata_for_version("1.0.0")
	assert result == {'filename': 'test_app-1.0.0.exe', 'checksum': 'DUMMY_CHECKSUM', 'version': '1.0.0'}

def test_metadata_getting_newest():
	md = MetaData()
	assert len(md._metadata) == 0
	md.add_metadata("test_app-1.0.0.exe", "DUMMY_CHECKSUM", "1.0.0")
	assert len(md._metadata) == 1
	assert md.get_newest(MetaDataChannel.STABLE) == Version("1.0.0")
	
	md.add_metadata("test_app-1.0.0a1.exe", "DUMMY_CHECKSUM_FOR_ALPHA", "1.0.0a1")
	assert len(md._metadata) == 2
	assert md.get_newest(MetaDataChannel.ALPHA) == Version("1.0.0a1")
	
	md.add_metadata("test_app-1.0.0b1.exe", "DUMMY_CHECKSUM_FOR_BETA", "1.0.0b1")
	assert len(md._metadata) == 3
	assert md.get_newest(MetaDataChannel.BETA) == Version("1.0.0b1")
