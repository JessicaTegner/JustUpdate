"""This tests the justupdate/repo/version.py file"""

from . import util
from justupdate.repo.version import Version

def test_version_equality():
	assert Version("1.0.0") == Version("1.0.0")
	assert Version("1.0.0b1") == Version("1.0.0b1")
	assert Version("1.0.0a1") == Version("1.0.0a1")

def test_version_inequality():
	assert Version("1.0.0") != Version("1.0.0b1")
	assert Version("1.0.0b1") != Version("1.0.0a1")
	assert Version("1.0.0a1") != Version("1.0.0")

def test_version_greater_than():
	assert Version("1.0.2") > Version("1.0.1")
	assert Version("1.2.0") > Version("1.1.0")
	assert Version("2.0.0") > Version("1.0.0")

def test_less_than():
	assert Version("1.0.1") < Version("1.0.2")
	assert Version("1.1.0") < Version("1.2.0")
	assert Version("1.0.0") < Version("2.0.0")

def test_internal_representation():
	v1 = Version("1.2.3")
	v2 = Version("1.2.3b4")
	v3 = Version("1.2.3a4")
	
	assert v1.raw_version == ["1","2","3"]
	assert v2.raw_version == ["1","2","3", "4"]
	assert v3.raw_version == ["1","2","3", "0", "4"]

def test_human_readability():
	v1 = Version("1.2.3")
	v2 = Version("1.2.3b4")
	v3 = Version("1.2.3a4")
	
	assert v1.to_human_readable() == "1.2.3"
	assert v2.to_human_readable() == "1.2.3 beta 4"
	assert v3.to_human_readable() == "1.2.3 alpha 4"

